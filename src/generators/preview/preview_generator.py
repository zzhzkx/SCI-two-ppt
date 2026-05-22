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
        """从PPTX文件生成HTML预览（保持样式一致）."""
        converter = PptxToHtmlConverter(pptx_path)
        html_path = self.output_dir / f"slide_{slide_index}.html"
        converter.save_html(slide_index, str(html_path))
        return str(html_path)

    def generate_html_preview(self, slide_data: dict, slide_index: int) -> str:
        """生成HTML预览文件（从蓝图数据）."""
        title = slide_data.get("title", f"Slide {slide_index}")
        content = slide_data.get("content", "")
        html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{title}</title></head>
<body>
<h1>{title}</h1>
<p>{content}</p>
</body>
</html>"""
        html_path = self.output_dir / f"slide_{slide_index}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        return str(html_path)
