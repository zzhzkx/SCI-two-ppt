"""图表提取器 - 从PDF中提取图片和表格."""

import fitz  # PyMuPDF
from pathlib import Path
import json
from typing import Optional
import re


async def extract_figures(pdf_path: str, output_dir: str = None) -> list[dict]:
    """提取PDF中的图表。

    Args:
        pdf_path: PDF文件路径
        output_dir: 图片输出目录（默认为 workspace/assets/figures）

    Returns:
        list[dict]: [{"path": str, "caption": str, "type": "figure|table", "page": int}]
    """
    p = Path(pdf_path)
    if not p.exists():
        raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")

    if output_dir is None:
        output_dir = str(Path("workspace/assets/figures"))

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    figures = []
    doc = fitz.open(str(p))

    for page_num in range(len(doc)):
        page = doc[page_num]

        # 提取图片
        image_figures = await _extract_images_from_page(page, page_num, output_dir, p.stem)
        figures.extend(image_figures)

        # 提取表格（基于文本检测）
        table_figures = await _extract_tables_from_page(page, page_num, p.stem)
        figures.extend(table_figures)

    doc.close()

    return figures


async def _extract_images_from_page(
    page: fitz.Page,
    page_num: int,
    output_dir: str,
    pdf_stem: str
) -> list[dict]:
    """从单页提取图片."""
    figures = []
    image_list = page.get_images()

    for img_idx, img in enumerate(image_list):
        try:
            # 获取图片数据
            xref = img[0]
            base_image = page.parent.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            # 保存图片
            image_filename = f"{pdf_stem}_page{page_num}_fig{img_idx}.{image_ext}"
            image_path = Path(output_dir) / image_filename

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            # 尝试提取图片标题（在图片下方查找）
            caption = await _find_figure_caption(page, img_idx)

            figures.append({
                "path": str(image_path),
                "caption": caption,
                "type": "figure",
                "page": page_num
            })

        except Exception as e:
            # 跳过无法提取的图片
            continue

    return figures


async def _extract_tables_from_page(
    page: fitz.Page,
    page_num: int,
    pdf_stem: str
) -> list[dict]:
    """从单页提取表格（基于文本布局检测）."""
    tables = []
    text = page.get_text()

    # 简单的表格检测：查找包含多个连续数字或对齐文本的区域
    lines = text.split('\n')
    table_candidates = []
    current_table = []

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            if current_table:
                table_candidates.append('\n'.join(current_table))
                current_table = []
            continue

        # 检测可能是表格行的特征
        if _is_table_row(line_stripped):
            current_table.append(line_stripped)
        else:
            if current_table and len(current_table) >= 3:
                table_candidates.append('\n'.join(current_table))
            current_table = []

    # 处理最后一个表格
    if current_table and len(current_table) >= 3:
        table_candidates.append('\n'.join(current_table))

    # 为每个表格创建记录
    for idx, table_text in enumerate(table_candidates):
        caption = f"Table detected on page {page_num + 1}"

        # 查找表格标题
        table_caption = await _find_table_caption(text, table_text)
        if table_caption:
            caption = table_caption

        tables.append({
            "path": "",  # 表格没有单独的图片文件
            "caption": caption,
            "type": "table",
            "page": page_num,
            "content": table_text[:500]  # 保存表格内容
        })

    return tables


def _is_table_row(line: str) -> bool:
    """判断一行是否是表格行."""
    # 包含多个数字（可能是数据行）
    numbers = re.findall(r'\d+\.?\d*', line)
    if len(numbers) >= 3:
        return True

    # 包含制表符或多空格分隔
    if '\t' in line or '  ' in line:
        # 检查是否是对齐的数据
        parts = re.split(r'\s{2,}|\t', line)
        if len(parts) >= 3:
            return True

    return False


async def _find_figure_caption(page: fitz.Page, figure_index: int) -> str:
    """查找图片标题."""
    text = page.get_text()
    lines = text.split('\n')

    # 查找 "Figure X" 或 "Fig. X" 模式
    for i, line in enumerate(lines):
        if re.match(r'^(Figure|Fig\.?)\s*\d+', line, re.IGNORECASE):
            # 标题可能跨多行
            caption = line.strip()
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not next_line.startswith(('Figure', 'Fig')):
                    caption += " " + next_line
            return caption

    return f"Figure {figure_index + 1}"


async def _find_table_caption(text: str, table_content: str) -> str:
    """查找表格标题."""
    lines = text.split('\n')

    # 查找 "Table X" 模式
    for i, line in enumerate(lines):
        if re.match(r'^(Table)\s*\d+', line, re.IGNORECASE):
            caption = line.strip()
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not next_line.startswith('Table'):
                    caption += " " + next_line
            return caption

    return ""
