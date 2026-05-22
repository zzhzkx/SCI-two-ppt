"""SCI-two-ppt MCP Server entry point.

Exposes 6 tools for Claude Code to orchestrate the paper-to-PPT workflow.
"""

from mcp.server.fastmcp import FastMCP
import json
from pathlib import Path

from src.core.config import load_config
from src.core.workspace import Workspace

mcp = FastMCP("sci-two-ppt")
config = load_config()


@mcp.tool()
def parse_papers(papers: list[str], workspace_path: str = "") -> str:
    """Parse scientific paper PDFs and extract structured content.

    Args:
        papers: List of PDF file paths to parse.
        workspace_path: Optional workspace directory path.

    Returns:
        JSON with extracted paper structure (title, abstract, methods,
        results, figures, tables, key_findings, innovations) and quality report.
    """
    ws = Workspace(workspace_path or config.default_workspace)
    ws.ensure_exists()

    results = []
    for paper_path in papers:
        p = Path(paper_path)
        if not p.exists():
            results.append({"path": paper_path, "error": f"File not found: {paper_path}"})
            continue

        if p.suffix.lower() != ".pdf":
            results.append({"path": paper_path, "error": f"Not a PDF: {paper_path}"})
            continue

        # TODO: Implement PyMuPDF-based parsing in Milestone 2
        results.append({
            "path": paper_path,
            "title": f"[Mock] {p.stem}",
            "abstract": "[Mock] Abstract placeholder - will be extracted from PDF",
            "methods": "[Mock] Methods section placeholder",
            "results": "[Mock] Results section placeholder",
            "figures": [],
            "tables": [],
            "key_findings": ["[Mock] Key finding 1"],
            "innovations": ["[Mock] Innovation 1"],
        })

    return json.dumps({
        "papers": results,
        "quality_report": "[Mock] Quality analysis will be implemented in Milestone 2",
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def build_goal(paper_analysis: str, requirements: str, workspace_path: str = "") -> str:
    """Build a structured goal document from paper analysis and user requirements.

    Args:
        paper_analysis: JSON string from parse_papers output.
        requirements: User requirements text (from multi-round dialogue).
        workspace_path: Optional workspace directory path.

    Returns:
        JSON with goal_content (full goal.md), sections list, and slide count estimate.
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
    """Execute a sub-agent task for PPT content preparation.

    Args:
        agent_type: One of "content_extract", "visual_resources", "ui_design", "speaker_notes".
        goal: The goal.md content.
        context: JSON string with results from prerequisite agents.
        workspace_path: Optional workspace directory path.

    Returns:
        JSON with agent_type, result_md (markdown output), and assets (image paths).
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
def generate_blueprint(goal: str, agent_results: str, workspace_path: str = "") -> str:
    """Generate a detailed PPT blueprint from goal and agent results.

    Args:
        goal: The goal.md content.
        agent_results: JSON string containing all sub-agent results.
        workspace_path: Optional workspace directory path.

    Returns:
        JSON with blueprint_yaml (full YAML blueprint) and slide_count.
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
    """Build a single slide and generate HTML preview.

    Args:
        blueprint: The blueprint YAML content.
        slide_index: Which slide to build (0-based).
        modifications: Optional user modification notes to apply.
        workspace_path: Optional workspace directory path.

    Returns:
        JSON with slide_index, preview_html path, and preview_image path.
    """
    ws = Workspace(workspace_path or config.default_workspace)
    ws.ensure_exists()

    # TODO: Implement python-pptx slide building + HTML preview in Milestone 5
    return json.dumps({
        "slide_index": slide_index,
        "preview_html": str(ws.path / "preview" / f"slide_{slide_index}.html"),
        "preview_image": "",
        "status": "[Mock] Slide building will be implemented in Milestone 5",
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def generate_pptx(
    blueprint: str,
    slide_dir: str = "",
    output_path: str = "",
    workspace_path: str = "",
) -> str:
    """Generate the final PPTX file from confirmed slides.

    Args:
        blueprint: The blueprint YAML content.
        slide_dir: Directory with confirmed slide files.
        output_path: Output path for the final .pptx file.
        workspace_path: Optional workspace directory path.

    Returns:
        JSON with pptx_path, report_md (production report), and slide_count.
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


if __name__ == "__main__":
    mcp.run()
