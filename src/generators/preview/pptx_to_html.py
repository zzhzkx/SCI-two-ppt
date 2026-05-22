"""PPTX到HTML转换器 - 实现预览与PPTX一致."""

from pptx import Presentation
from pathlib import Path


class PptxToHtmlConverter:
    """将PPTX文件转换为HTML预览，保持样式一致."""

    def __init__(self, pptx_path: str):
        self.pptx_path = Path(pptx_path)
        self.prs = Presentation(pptx_path)

    def convert_slide_to_html(self, slide_index: int) -> str:
        """将单页幻灯片转换为HTML."""
        if slide_index >= len(self.prs.slides):
            return "<html><body>Slide not found</body></html>"

        slide = self.prs.slides[slide_index]
        slide_width = self.prs.slide_width
        slide_height = self.prs.slide_height

        background_html = self._extract_background(slide)
        shapes_html = self._extract_shapes(slide)

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Slide {slide_index}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
        .slide-container {{
            width: {self._emu_to_px(slide_width)}px;
            height: {self._emu_to_px(slide_height)}px;
            margin: 0 auto;
            position: relative;
            overflow: hidden;
            {background_html}
        }}
        .shape {{ position: absolute; word-wrap: break-word; }}
    </style>
</head>
<body>
    <div class="slide-container">
        {shapes_html}
    </div>
</body>
</html>"""
        return html

    def _extract_background(self, slide) -> str:
        background = slide.background
        fill = background.fill
        if fill.type is not None:
            if fill.type == 1:  # Solid
                color = fill.fore_color.rgb
                return f"background: #{color};"
        return "background: #FFFFFF;"

    def _extract_shapes(self, slide) -> str:
        html_parts = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                left = self._emu_to_px(shape.left)
                top = self._emu_to_px(shape.top)
                width = self._emu_to_px(shape.width)
                height = self._emu_to_px(shape.height)
                text = shape.text_frame.text
                font_size = self._get_font_size(shape)
                font_color = self._get_font_color(shape)
                alignment = self._get_alignment(shape)
                bold = self._is_bold(shape)

                style = f"left:{left}px; top:{top}px; width:{width}px; height:{height}px;"
                style += f" font-size:{font_size}px; color:{font_color};"
                style += f" text-align:{alignment};"
                if bold:
                    style += " font-weight:bold;"

                html_parts.append(f'<div class="shape" style="{style}">{text}</div>')

        return "\n        ".join(html_parts)

    def _emu_to_px(self, emu: int) -> int:
        return int(emu * 96 / 914400)

    def _get_font_size(self, shape) -> int:
        try:
            if shape.text_frame.paragraphs[0].runs:
                run = shape.text_frame.paragraphs[0].runs[0]
                if run.font.size:
                    return int(run.font.size.pt)
        except:
            pass
        return 18

    def _get_font_color(self, shape) -> str:
        try:
            if shape.text_frame.paragraphs[0].runs:
                run = shape.text_frame.paragraphs[0].runs[0]
                if run.font.color and run.font.color.rgb:
                    return f"#{run.font.color.rgb}"
        except:
            pass
        return "#000000"

    def _get_alignment(self, shape) -> str:
        try:
            para = shape.text_frame.paragraphs[0]
            if para.alignment == 1:  # CENTER
                return "center"
            elif para.alignment == 2:  # RIGHT
                return "right"
        except:
            pass
        return "left"

    def _is_bold(self, shape) -> bool:
        try:
            if shape.text_frame.paragraphs[0].runs:
                run = shape.text_frame.paragraphs[0].runs[0]
                return run.font.bold
        except:
            pass
        return False

    def save_html(self, slide_index: int, output_path: str):
        html = self.convert_slide_to_html(slide_index)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
