"""SCI-two-ppt MCP Server entry point.

Exposes 11 tools for Claude Code to orchestrate the paper-to-PPT workflow.
"""

from mcp.server.fastmcp import FastMCP
import json
import asyncio
from pathlib import Path

from src.core.config import load_config
from src.core.workspace import Workspace
from src.parsers.paper_parser import parse_papers as _parse_papers
from src.parsers.figure_extractor import extract_figures as _extract_figures

mcp = FastMCP("sci-two-ppt")
config = load_config()


@mcp.tool()
def parse_papers(papers: list[str], workspace_path: str = "") -> str:
    """解析论文PDF，提取结构化内容。

    Input: papers - PDF文件路径列表
    Output: JSON {
        "papers": [{
            "path": str,
            "title": str,
            "abstract": str,
            "methods": str,
            "results": str,
            "figures": [{"path": str, "caption": str}],
            "key_findings": [str],
            "innovations": [str]
        }],
        "quality_report": str
    }
    """
    ws = Workspace(workspace_path or config.default_workspace)
    ws.ensure_exists()

    try:
        result = asyncio.run(_parse_papers(papers))
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)


@mcp.tool()
def extract_figures(pdf_path: str, output_dir: str = "", workspace_path: str = "") -> str:
    """提取论文PDF中的图表和图片。

    Input: pdf_path - PDF文件路径, output_dir - 图片输出目录
    Output: JSON {
        "figures": [{"path": str, "caption": str, "type": "figure|table", "page": int}]
    }
    """
    ws = Workspace(workspace_path or config.default_workspace)
    ws.ensure_exists()

    output_dir = output_dir or str(ws.path / "assets" / "figures")

    try:
        figures = asyncio.run(_extract_figures(pdf_path, output_dir))
        return json.dumps({"figures": figures}, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)


@mcp.tool()
def build_goal(paper_analysis: str, requirements: str, workspace_path: str = "") -> str:
    """构建结构化的PPT目标文档。

    Input: paper_analysis - parse_papers输出的JSON, requirements - 用户需求文本
    Output: JSON {
        "goal_content": str,
        "sections": [str],
        "slide_count_estimate": int
    }
    """
    ws = Workspace(workspace_path or config.default_workspace)
    ws.ensure_exists()

    # TODO: Implement goal.md generation in Milestone 3
    goal_content = f"""# PPT Goal Document

## Paper Analysis Summary
{paper_analysis[:500]}

## Requirements
{requirements}

## Sections
1. Title & Introduction
2. Background & Motivation
3. Methods
4. Results & Discussion
5. Conclusion & Future Work

## Notes
[Mock] This goal document will be properly generated in Milestone 3.
"""
    return json.dumps({
        "goal_content": goal_content,
        "sections": ["Title", "Background", "Methods", "Results", "Conclusion"],
        "slide_count_estimate": 12,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def run_subagent(
    agent_type: str,
    goal: str,
    context: str = "{}",
    workspace_path: str = "",
) -> str:
    """执行子Agent任务。

    Input: agent_type - Agent类型(content_extract/visual_resources/ui_design/speaker_notes),
           goal - goal.md内容, context - 上下文JSON
    Output: JSON {
        "agent_type": str,
        "result_md": str,
        "assets": [str]
    }
    """
    valid_types = ["content_extract", "visual_resources", "ui_design", "speaker_notes"]
    if agent_type not in valid_types:
        return json.dumps({"error": f"Invalid agent_type: {agent_type}. Must be one of {valid_types}"})

    ws = Workspace(workspace_path or config.default_workspace)
    ws.ensure_exists()

    # TODO: Implement actual agent logic in Milestone 4
    return json.dumps({
        "agent_type": agent_type,
        "result_md": f"[Mock] {agent_type} agent result - will be implemented in Milestone 4",
        "assets": [],
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def read_pptx(pptx_path: str, workspace_path: str = "") -> str:
    """读取PPTX文件状态，获取幻灯片信息。

    Input: pptx_path - PPTX文件路径
    Output: JSON {
        "slide_count": int,
        "slides": [{"index": int, "shapes": [{"name": str, "type": str, "text": str}]}]
    }
    """
    from pptx import Presentation

    try:
        prs = Presentation(pptx_path)
        slides_info = []

        for idx, slide in enumerate(prs.slides):
            shapes_info = []
            for shape in slide.shapes:
                shape_info = {
                    "name": shape.name,
                    "type": str(shape.shape_type),
                    "text": shape.text if shape.has_text_frame else ""
                }
                shapes_info.append(shape_info)

            slides_info.append({
                "index": idx,
                "shapes": shapes_info
            })

        return json.dumps({
            "slide_count": len(prs.slides),
            "slides": slides_info
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)


@mcp.tool()
def diff_pptx(original: str, modified: str, workspace_path: str = "") -> str:
    """对比两版PPTX的差异，检测用户手动修改。

    Input: original - 原版PPTX路径, modified - 修改后PPTX路径
    Output: JSON {
        "changes": [{"slide_index": int, "type": str, "detail": str}],
        "summary": str
    }
    """
    from pptx import Presentation

    try:
        prs_orig = Presentation(original)
        prs_mod = Presentation(modified)

        changes = []

        # 比较幻灯片数量
        if len(prs_orig.slides) != len(prs_mod.slides):
            changes.append({
                "slide_index": -1,
                "type": "slide_count",
                "detail": f"幻灯片数量从 {len(prs_orig.slides)} 变为 {len(prs_mod.slides)}"
            })

        # 逐页比较
        for idx in range(min(len(prs_orig.slides), len(prs_mod.slides))):
            slide_orig = prs_orig.slides[idx]
            slide_mod = prs_mod.slides[idx]

            # 比较文本内容
            for shape_orig, shape_mod in zip(slide_orig.shapes, slide_mod.shapes):
                if shape_orig.has_text_frame and shape_mod.has_text_frame:
                    if shape_orig.text != shape_mod.text:
                        changes.append({
                            "slide_index": idx,
                            "type": "text",
                            "detail": f"形状 '{shape_orig.name}' 文本已修改"
                        })

                # 比较位置和大小
                if (shape_orig.left != shape_mod.left or
                    shape_orig.top != shape_mod.top or
                    shape_orig.width != shape_mod.width or
                    shape_orig.height != shape_mod.height):
                    changes.append({
                        "slide_index": idx,
                        "type": "position",
                        "detail": f"形状 '{shape_orig.name}' 位置/大小已修改"
                    })

        summary = f"共检测到 {len(changes)} 处变化"
        if not changes:
            summary = "未检测到明显变化"

        return json.dumps({
            "changes": changes,
            "summary": summary
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False, indent=2)


@mcp.tool()
def generate_blueprint(goal: str, agent_results: str, workspace_path: str = "") -> str:
    """生成详细的PPT蓝图。

    Input: goal - goal.md内容, agent_results - Agent结果JSON
    Output: JSON {
        "blueprint_yaml": str,
        "slide_count": int
    }
    """
    ws = Workspace(workspace_path or config.default_workspace)
    ws.ensure_exists()

    # TODO: Implement blueprint generation in Milestone 5
    blueprint = """# PPT Blueprint
slides:
  - index: 0
    type: title
    title: "[Mock] Title Slide"
    subtitle: "[Mock] Subtitle"
    notes: "Welcome and introduction"
    duration_seconds: 30

  - index: 1
    type: content
    title: "[Mock] Content Slide"
    content: "[Mock] Main content"
    notes: "Explain key points"
    duration_seconds: 120
"""
    return json.dumps({
        "blueprint_yaml": blueprint,
        "slide_count": 2,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def build_slide(
    blueprint: str,
    slide_index: int,
    modifications: str = "",
    workspace_path: str = "",
) -> str:
    """根据蓝图生成单页幻灯片。

    Input: blueprint - 蓝图YAML, slide_index - 页码(从0开始), modifications - 修改意见
    Output: JSON {
        "slide_index": int,
        "pptx_path": str,
        "preview_image": str
    }
    """
    ws = Workspace(workspace_path or config.default_workspace)
    ws.ensure_exists()

    # TODO: Implement python-pptx slide building + HTML preview in Milestone 5
    return json.dumps({
        "slide_index": slide_index,
        "pptx_path": str(ws.path / "preview" / f"slide_{slide_index}.pptx"),
        "preview_image": "",
        "status": "[Mock] Slide building will be implemented in Milestone 5",
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def render_preview(pptx_path: str, slide_index: int, workspace_path: str = "") -> str:
    """渲染幻灯片为预览图片。

    Input: pptx_path - PPTX文件路径, slide_index - 页码
    Output: JSON {
        "preview_image": str
    }
    """
    ws = Workspace(workspace_path or config.default_workspace)
    ws.ensure_exists()

    # TODO: Implement preview rendering in Milestone 5
    return json.dumps({
        "preview_image": str(ws.path / "preview" / f"slide_{slide_index}.png"),
        "status": "[Mock] Preview rendering will be implemented in Milestone 5",
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def generate_pptx(
    blueprint: str,
    slide_dir: str = "",
    output_path: str = "",
    workspace_path: str = "",
) -> str:
    """最终打包生成PPTX文件。

    Input: blueprint - 蓝图YAML, slide_dir - 确认的幻灯片目录, output_path - 输出路径
    Output: JSON {
        "pptx_path": str,
        "report_md": str,
        "slide_count": int
    }
    """
    ws = Workspace(workspace_path or config.default_workspace)
    ws.ensure_exists()

    # TODO: Implement final PPTX generation in Milestone 5
    return json.dumps({
        "pptx_path": output_path or str(ws.path / "output.pptx"),
        "report_md": "[Mock] Production report will be generated in Milestone 5",
        "slide_count": 0,
        "status": "[Mock] PPTX generation will be implemented in Milestone 5",
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def get_academic_style(domain: str = "general", workspace_path: str = "") -> str:
    """获取学术PPT规范（配色、字体、排版）。

    Input: domain - 领域(optics/physics/chemistry/computer_science/general)
    Output: JSON {
        "primary_color": str,
        "secondary_color": str,
        "font_family": str,
        "font_sizes": {"title": int, "subtitle": int, "body": int},
        "margins": {"top": int, "bottom": int, "left": int, "right": int}
    }
    """
    # TODO: Implement academic style library in Milestone 4
    styles = {
        "optics": {
            "primary_color": "#003366",
            "secondary_color": "#6699CC",
            "font_family": "Arial",
            "font_sizes": {"title": 36, "subtitle": 24, "body": 18},
            "margins": {"top": 1, "bottom": 1, "left": 1.2, "right": 1.2}
        },
        "physics": {
            "primary_color": "#2C3E50",
            "secondary_color": "#3498DB",
            "font_family": "Calibri",
            "font_sizes": {"title": 36, "subtitle": 24, "body": 18},
            "margins": {"top": 1, "bottom": 1, "left": 1.2, "right": 1.2}
        },
        "general": {
            "primary_color": "#1A5276",
            "secondary_color": "#2E86C1",
            "font_family": "Arial",
            "font_sizes": {"title": 36, "subtitle": 24, "body": 18},
            "margins": {"top": 1, "bottom": 1, "left": 1.2, "right": 1.2}
        }
    }

    style = styles.get(domain, styles["general"])
    return json.dumps(style, ensure_ascii=False, indent=2)


@mcp.tool()
def get_slide_template(slide_type: str, workspace_path: str = "") -> str:
    """获取页面模板定义。

    Input: slide_type - 页面类型(title/content/chart/conclusion)
    Output: JSON {
        "layout": str,
        "elements": [...],
        "suggested_duration": int
    }
    """
    # TODO: Implement slide template library in Milestone 5
    templates = {
        "title": {
            "layout": "title_slide",
            "elements": ["title", "subtitle", "author", "date"],
            "suggested_duration": 30
        },
        "content": {
            "layout": "content_slide",
            "elements": ["title", "content_blocks", "figures"],
            "suggested_duration": 120
        },
        "chart": {
            "layout": "chart_slide",
            "elements": ["title", "chart", "explanation"],
            "suggested_duration": 90
        },
        "conclusion": {
            "layout": "conclusion_slide",
            "elements": ["title", "key_points", "future_work"],
            "suggested_duration": 60
        }
    }

    template = templates.get(slide_type, templates["content"])
    return json.dumps(template, ensure_ascii=False, indent=2)


@mcp.tool()
def get_citation_format(format_type: str = "IEEE", workspace_path: str = "") -> str:
    """获取引用格式规范。

    Input: format_type - 格式(IEEE/APA/MLA)
    Output: JSON {
        "inline_format": str,
        "reference_format": str,
        "examples": [str]
    }
    """
    # TODO: Implement citation format library in Milestone 4
    formats = {
        "IEEE": {
            "inline_format": "[{number}]",
            "reference_format": "{author}, \"{title},\" {journal}, vol. {volume}, no. {issue}, pp. {pages}, {year}.",
            "examples": ["[1] A. Author, \"Title,\" Journal, vol. 1, no. 2, pp. 10-20, 2024."]
        },
        "APA": {
            "inline_format": "({author}, {year})",
            "reference_format": "{author} ({year}). {title}. {journal}, {volume}({issue}), {pages}.",
            "examples": ["Author, A. (2024). Title. Journal, 1(2), 10-20."]
        },
        "MLA": {
            "inline_format": "({author} {page})",
            "reference_format": "{author}. \"{title}.\" {journal}, vol. {volume}, no. {issue}, {year}, pp. {pages}.",
            "examples": ["Author, A. \"Title.\" Journal, vol. 1, no. 2, 2024, pp. 10-20."]
        }
    }

    fmt = formats.get(format_type, formats["IEEE"])
    return json.dumps(fmt, ensure_ascii=False, indent=2)


@mcp.tool()
def cleanup_workspace(workspace_path: str = "") -> str:
    """整理清理工作空间，移除中间文件。

    Input: workspace_path - 工作空间路径
    Output: JSON {
        "cleaned_files": [str],
        "kept_files": [str],
        "report": str
    }
    """
    ws = Workspace(workspace_path or config.default_workspace)

    if not ws.path.exists():
        return json.dumps({"report": "工作空间不存在"}, ensure_ascii=False, indent=2)

    cleaned = []
    kept = []

    # 清理中间文件
    intermediate_dirs = ["agent_results", "preview"]
    for dir_name in intermediate_dirs:
        dir_path = ws.path / dir_name
        if dir_path.exists():
            for f in dir_path.rglob("*"):
                if f.is_file():
                    cleaned.append(str(f.relative_to(ws.path)))
                    f.unlink()

    # 保留重要文件
    important_files = ["output.pptx", "goal.md", "requirements.md", "production_report.md"]
    for file_name in important_files:
        file_path = ws.path / file_name
        if file_path.exists():
            kept.append(file_name)

    report = f"清理完成: 删除 {len(cleaned)} 个文件, 保留 {len(kept)} 个重要文件"

    return json.dumps({
        "cleaned_files": cleaned[:50],  # 限制显示数量
        "kept_files": kept,
        "report": report
    }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
