"""单页幻灯片生成器 - 基于python-pptx."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import yaml
from pathlib import Path


def _hex_to_rgb(hex_color: str) -> tuple:
    """将十六进制颜色转换为RGB元组."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


async def build_slide(
    blueprint_yaml: str,
    slide_index: int,
    modifications: str = "",
    template_path: str = None
) -> dict:
    """根据蓝图生成单页幻灯片."""
    blueprint = yaml.safe_load(blueprint_yaml)

    if slide_index >= len(blueprint.get("slides", [])):
        raise ValueError(f"Slide index {slide_index} out of range")

    slide_def = blueprint["slides"][slide_index]
    design = slide_def.get("design", {})

    # 创建或使用模板
    if template_path and Path(template_path).exists():
        prs = Presentation(template_path)
    else:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)

    # 清空默认幻灯片
    while len(prs.slides) > 0:
        rId = prs.slides._sldIdLst[0].get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        prs.part.drop_rel(rId)
        prs.slides._sldIdLst.remove(prs.slides._sldIdLst[0])

    # 添加幻灯片
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # 设置背景
    _apply_background(slide, design)

    # 根据类型填充内容
    slide_type = slide_def.get("type", "content")

    if slide_type == "title":
        _build_title_slide(slide, slide_def, design)
    elif slide_type == "content":
        _build_content_slide(slide, slide_def, design)
    elif slide_type == "chart":
        _build_chart_slide(slide, slide_def, design)
    elif slide_type == "conclusion":
        _build_conclusion_slide(slide, slide_def, design)
    else:
        _build_content_slide(slide, slide_def, design)

    # 保存
    output_dir = Path("workspace/preview")
    output_dir.mkdir(parents=True, exist_ok=True)
    pptx_path = output_dir / f"slide_{slide_index}.pptx"
    prs.save(str(pptx_path))

    return {
        "pptx_path": str(pptx_path),
        "slide_index": slide_index
    }


def _apply_background(slide, design: dict):
    """应用背景样式."""
    bg_type = design.get("background", "white")

    if bg_type == "gradient":
        colors = design.get("background_colors", ["#0D2137", "#1B6CA8"])
        fill = slide.background.fill
        fill.gradient()
        fill.gradient_stops[0].color.rgb = RGBColor(*_hex_to_rgb(colors[0]))
        fill.gradient_stops[0].position = 0.0
        fill.gradient_stops[1].color.rgb = RGBColor(*_hex_to_rgb(colors[1]))
        fill.gradient_stops[1].position = 1.0
    elif bg_type == "solid":
        color = design.get("background_color", "#FFFFFF")
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(*_hex_to_rgb(color))


def _build_title_slide(slide, slide_def: dict, design: dict):
    """构建封面页."""
    title = slide_def.get("title", "")
    subtitle = slide_def.get("subtitle", "")

    title_size = design.get("title_font_size", 48)
    title_color = design.get("title_color", "#FFFFFF")
    sub_size = design.get("subtitle_font_size", 28)
    sub_color = design.get("subtitle_color", "#6699CC")

    # 标题 - 居中
    left, top, width, height = Inches(1), Inches(2.5), Inches(11), Inches(1.5)
    title_box = slide.shapes.add_textbox(left, top, width, height)
    title_frame = title_box.text_frame
    title_frame.word_wrap = True
    title_para = title_frame.paragraphs[0]
    title_para.text = title
    title_para.font.size = Pt(title_size)
    title_para.font.bold = True
    title_para.font.color.rgb = RGBColor(*_hex_to_rgb(title_color))
    title_para.alignment = PP_ALIGN.CENTER

    # 副标题 - 居中
    left, top, width, height = Inches(1), Inches(4), Inches(11), Inches(1)
    sub_box = slide.shapes.add_textbox(left, top, width, height)
    sub_frame = sub_box.text_frame
    sub_frame.word_wrap = True
    sub_para = sub_frame.paragraphs[0]
    sub_para.text = subtitle
    sub_para.font.size = Pt(sub_size)
    sub_para.font.color.rgb = RGBColor(*_hex_to_rgb(sub_color))
    sub_para.alignment = PP_ALIGN.CENTER


def _build_content_slide(slide, slide_def: dict, design: dict):
    """构建内容页."""
    title = slide_def.get("title", "")
    content = slide_def.get("content", "")

    # 标题
    left, top, width, height = Inches(0.5), Inches(0.3), Inches(12), Inches(1)
    title_box = slide.shapes.add_textbox(left, top, width, height)
    title_frame = title_box.text_frame
    title_frame.text = title
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True

    # 内容
    left, top, width, height = Inches(0.5), Inches(1.5), Inches(12), Inches(5.5)
    content_box = slide.shapes.add_textbox(left, top, width, height)
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    content_para = content_frame.paragraphs[0]
    content_para.text = content
    content_para.font.size = Pt(18)


def _build_chart_slide(slide, slide_def: dict, design: dict):
    """构建图表页."""
    title = slide_def.get("title", "")
    chart_desc = slide_def.get("chart", "")

    left, top, width, height = Inches(0.5), Inches(0.3), Inches(12), Inches(1)
    title_box = slide.shapes.add_textbox(left, top, width, height)
    title_frame = title_box.text_frame
    title_frame.text = title
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True

    left, top, width, height = Inches(0.5), Inches(1.5), Inches(12), Inches(5.5)
    desc_box = slide.shapes.add_textbox(left, top, width, height)
    desc_frame = desc_box.text_frame
    desc_frame.text = chart_desc
    desc_para = desc_frame.paragraphs[0]
    desc_para.font.size = Pt(18)


def _build_conclusion_slide(slide, slide_def: dict, design: dict):
    """构建总结页."""
    title = slide_def.get("title", "Conclusion")

    left, top, width, height = Inches(0.5), Inches(2), Inches(12), Inches(1.5)
    title_box = slide.shapes.add_textbox(left, top, width, height)
    title_frame = title_box.text_frame
    title_para = title_frame.paragraphs[0]
    title_para.text = title
    title_para.font.size = Pt(44)
    title_para.font.bold = True
    title_para.alignment = PP_ALIGN.CENTER
