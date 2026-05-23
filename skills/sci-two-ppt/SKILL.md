# sci-two-ppt Skill

将科研论文转换为专业学术PPT的工具。

## 核心架构

```
Claude Code (大脑)
    |
    +-- 10步工作流编排
    +-- 多轮对话收集需求
    +-- 批判性审查
    +-- 子Agent并行执行
    |
    v
MCP Server (工具)
    |
    +-- 论文解析 (parse_papers)
    +-- SVG生成 (generate_svg_slide)
    +-- SVG转换 (svg_to_pptx)
    +-- 质量检查 (check_svg_quality)
    +-- 预览生成 (generate_preview_from_pptx)
```

## 10步工作流

| 步骤 | 角色 | 产出 |
|------|------|------|
| Step 1 | Paper Analyzer | analysis.json |
| Step 2 | Content Strategist | requirements.md |
| Step 3 | Content Strategist | goal.md |
| Step 4 | Professor + Quality Reviewer | review_reports |
| Step 5 | 7个子Agent并行 | agent_results/ |
| Step 6 | 用户确认 | 确认/修改 |
| Step 7 | Claude主Agent | blueprint.yaml |
| Step 8 | SVG Generator | 逐页PPT |
| Step 9 | MCP工具 | output_final.pptx |
| Step 10 | MCP工具 | 制作报告 |

## 7个核心角色

1. Paper Analyzer - 论文分析专家
2. Content Strategist - 内容策略师
3. Visual Designer - 视觉设计师
4. SVG Generator - SVG生成器
5. Quality Reviewer - 质量审查员
6. Professor Reviewer - 论文教授审查员
7. Material Collector - 素材搜集员

## MCP工具 (21个)

论文解析: parse_papers, extract_figures
SVG引擎: generate_svg_slide, generate_svg_chart, svg_to_pptx, check_svg_quality
PPT生成: build_slide, generate_pptx, read_pptx, diff_pptx
规范库: get_academic_style, get_slide_template, get_citation_format
预览系统: generate_preview, generate_preview_from_pptx, start_preview_server
反馈系统: detect_modifications, learn_feedback, get_feedback_patterns
工作空间: cleanup_workspace, get_latest_feedback
