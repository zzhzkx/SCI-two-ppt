"""预览生成器 - 生成HTML/图片/PPT预览."""

from pathlib import Path
import json
from .pptx_to_html import PptxToHtmlConverter


class PreviewGenerator:
    """预览生成器，支持多种预览格式."""

    def __init__(self, output_dir: str = "workspace/preview"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_html_from_pptx(self, pptx_path: str, slide_index: int) -> str:
        """从PPTX文件生成HTML预览（保持样式一致）.

        Args:
            pptx_path: PPTX文件路径
            slide_index: 幻灯片索引

        Returns:
            HTML文件路径
        """
        converter = PptxToHtmlConverter(pptx_path)
        html_path = self.output_dir / f"slide_{slide_index}.html"
        converter.save_html(slide_index, str(html_path))
        return str(html_path)

    def generate_html_preview(self, slide_data: dict, slide_index: int) -> str:
        """生成HTML预览文件（从蓝图数据）.

        Args:
            slide_data: 幻灯片数据
            slide_index: 幻灯片索引

        Returns:
            HTML文件路径
        """
        html_content = self._create_html_template(slide_data, slide_index)
        html_path = self.output_dir / f"slide_{slide_index}.html"

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return str(html_path)

    def _create_html_template(self, slide_data: dict, slide_index: int) -> str:
        """创建HTML模板."""
        title = slide_data.get("title", f"Slide {slide_index}")
        content = slide_data.get("content", "")
        notes = slide_data.get("notes", "")
        duration = slide_data.get("duration_seconds", 60)

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{title} - Preview</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
        .slide-container {{ width: 960px; height: 540px; margin: 0 auto; background: #FFFFFF; border: 1px solid #ddd; padding: 40px; }}
        .slide-title {{ font-size: 36px; font-weight: bold; color: #003366; margin-bottom: 20px; text-align: center; }}
        .slide-content {{ font-size: 18px; line-height: 1.6; color: #333; }}
        .controls {{ margin-top: 20px; text-align: center; }}
        .btn {{ padding: 10px 20px; margin: 5px; cursor: pointer; border: none; border-radius: 4px; }}
        .btn-confirm {{ background: #27ae60; color: white; }}
        .btn-modify {{ background: #f39c12; color: white; }}
    </style>
</head>
<body>
    <div class="slide-container">
        <div class="slide-title">{title}</div>
        <div class="slide-content">{content}</div>
    </div>
    <div class="controls">
        <button class="btn btn-confirm" onclick="sendAction('confirm')">Confirm</button>
        <button class="btn btn-modify" onclick="sendAction('modify')">Modify</button>
    </div>
</body>
</html>"""
        return html

    def get_preview_list(self) -> list:
        """获取所有预览文件列表."""
        previews = []
        for file in self.output_dir.glob("slide_*.html"):
            index = int(file.stem.split("_")[1])
            previews.append({
                "index": index,
                "path": str(file),
                "type": "html"
            })
        return sorted(previews, key=lambda x: x["index"])
