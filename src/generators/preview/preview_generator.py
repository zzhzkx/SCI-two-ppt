"""预览生成器 - 生成HTML/图片/PPT预览."""

from pathlib import Path
import json


class PreviewGenerator:
    """预览生成器，支持多种预览格式."""

    def __init__(self, output_dir: str = "workspace/preview"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_html_preview(self, slide_data: dict, slide_index: int) -> str:
        """生成HTML预览文件."""
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
        body {{ font-family: Arial; margin: 20px; }}
        .slide {{ border: 1px solid #ccc; padding: 20px; min-height: 400px; }}
        .controls {{ margin-top: 20px; }}
        button {{ margin-right: 10px; padding: 10px 20px; cursor: pointer; }}
    </style>
</head>
<body>
    <h1>Slide {slide_index}</h1>
    <div class="slide">
        <h2>{title}</h2>
        <p>{content}</p>
    </div>
    <div class="controls">
        <button onclick="alert('confirm')">Confirm</button>
        <button onclick="alert('modify')">Modify</button>
        <button onclick="alert('skip')">Skip</button>
        <button onclick="alert('redo')">Redo</button>
    </div>
</body>
</html>"""
        return html
