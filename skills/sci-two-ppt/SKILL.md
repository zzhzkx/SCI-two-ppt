# sci-two-ppt Skill

将科研论文转换为专业学术PPT的工具。

## 核心架构

```
Claude Code (大脑) → MCP Server (工具) → PPTX输出
```

## 10步工作流

| 步骤 | 角色 | 产出 | 审核点 |
|------|------|------|--------|
| Step 1 | Paper Analyzer | analysis.json | 论文解析结果是否准确 |
| Step 2 | Content Strategist | requirements.md | 需求是否完整 |
| Step 3 | Content Strategist | goal.md | 目标文档是否合理 |
| Step 4 | Professor + Quality Reviewer | review_reports | 审查建议是否采纳 |
| Step 5 | 7个子Agent并行 | agent_results/ | 各Agent产出是否满意 |
| Step 6 | 用户确认 | 确认/修改 | 最终确认 |
| Step 7 | Claude主Agent | blueprint.yaml | 蓝图是否合理 |
| Step 8 | SVG Generator | 逐页PPT | 每页都需确认 |
| Step 9 | MCP工具 | output_final.pptx | 最终PPT确认 |
| Step 10 | MCP工具 | 制作报告 | 完成确认 |

**重要**：每一步完成后都必须暂停，等待用户审核确认后再继续下一步。

## 审核点说明

### Step 1 完成后
- 审核：论文解析结果是否准确
- 确认后：进入Step 2

### Step 2 完成后
- 审核：需求文档是否完整
- 确认后：进入Step 3

### Step 3 完成后
- 审核：目标文档是否合理
- 确认后：进入Step 4

### Step 4 完成后
- 审核：审查建议是否采纳
- 确认后：进入Step 5

### Step 5 完成后
- 审核：所有Agent产出是否满意
- 确认后：进入Step 6

### Step 6 完成后
- 审核：最终确认
- 确认后：进入Step 7

### Step 7 完成后
- 审核：蓝图是否合理
- 确认后：进入Step 8

### Step 8 完成后
- 审核：每一页PPT是否满意
- 确认后：进入Step 9

### Step 9 完成后
- 审核：最终PPT是否满意
- 确认后：进入Step 10

### Step 10 完成后
- 审核：最终产出是否完整
- 确认后：流程完成

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
