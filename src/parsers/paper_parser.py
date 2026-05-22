"""论文解析器 - 提取原始文本."""

import fitz  # PyMuPDF
from docx import Document
from pathlib import Path
import json


async def parse_papers(papers: list[str]) -> dict:
    """解析论文，提取原始文本。

    Args:
        papers: 文件路径列表（支持 .pdf 和 .docx）

    Returns:
        dict: 包含原始文本和基础元数据
    """
    results = []
    errors = []

    for paper_path in papers:
        p = Path(paper_path)

        if not p.exists():
            errors.append(f"文件不存在: {paper_path}")
            continue

        try:
            if p.suffix.lower() == ".pdf":
                result = await _extract_pdf_text(p)
            elif p.suffix.lower() in [".docx", ".doc"]:
                result = await _extract_docx_text(p)
            else:
                errors.append(f"不支持的文件格式: {p.suffix}")
                continue
            results.append(result)
        except Exception as e:
            errors.append(f"解析失败 {paper_path}: {str(e)}")

    return {
        "papers": results,
        "errors": errors,
        "total": len(results),
        "failed": len(errors)
    }


async def _extract_pdf_text(pdf_path: Path) -> dict:
    """从PDF提取原始文本."""
    doc = fitz.open(str(pdf_path))

    # 提取全文
    full_text = ""
    page_count = len(doc)

    for page in doc:
        full_text += page.get_text() + "\n\n"

    doc.close()

    return {
        "path": str(pdf_path),
        "format": "pdf",
        "raw_text": full_text.strip(),
        "page_count": page_count,
        "word_count": len(full_text.split()),
        "char_count": len(full_text)
    }


async def _extract_docx_text(docx_path: Path) -> dict:
    """从Word文档提取原始文本."""
    doc = Document(str(docx_path))

    # 提取全文
    paragraphs = []
    for para in doc.paragraphs:
        if para.text.strip():
            paragraphs.append(para.text)

    full_text = "\n".join(paragraphs)

    return {
        "path": str(docx_path),
        "format": "docx",
        "raw_text": full_text,
        "paragraph_count": len(paragraphs),
        "word_count": len(full_text.split()),
        "char_count": len(full_text)
    }
