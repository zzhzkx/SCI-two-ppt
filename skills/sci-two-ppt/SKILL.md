# sci-two-ppt Skill

将科研论文转换为专业学术PPT的工具。

## 核心架构

```
Claude Code (大脑)
    │
    ├─ 10步工作流编排
    ├─ 多轮对话收集需求
    ├─ 批判性审查
    └─ 子Agent并行执行
    │
    ▼
MCP Server (工具)
    │
    ├─ 论文解析 (parse_papers)
    ├─ SVG生成 (generate_svg_slide)
    ├─ SVG转换 (svg_to_pptx)
    ├─ 质量检查 (check_svg_quality)
    └─ 预览生成 (generate_preview_from_pptx)
```

## 10步工作流

| 步骤 | 角色 | 产出 |
|------|------|------|
| Step 1 | Paper Analyzer | analysis.json + search_queries.json |
| Step 2 | Content Strategist | requirements.md |
| Step 3 | Content Strategist | goal.md |
| Step 4 | Professor Reviewer + Quality Reviewer | review_reports |
| Step 5 | 7个子Agent并行 | agent_results/ + SVG文件 |
| Step 6 | 用户确认 | 确认/修改意见 |
| Step 7 | Claude主Agent | blueprint.yaml |
| Step 8 | SVG Generator + 用户 | 逐页PPT |
| Step 9 | MCP工具 | output_final.pptx |
| Step 10 | MCP工具 | 制作报告 |

## 7个核心角色

| 角色 | 职责 | 输入 | 输出 |
|------|------|------|------|
| Paper Analyzer | 论文分析 | 原始文本 | analysis.json |
| Content Strategist | 内容策略 | analysis + requirements | goal.md |
| Visual Designer | 视觉设计 | goal.md | spec_lock.md |
| SVG Generator | SVG生成 | blueprint + spec_lock | .svg文件 |
| Quality Reviewer | 质量审查 | 所有产出 | review_report |
| Professor Reviewer | 学术审查 | analysis + goal | expert_review |
| Material Collector | 素材搜集 | research_field | materials/ |

## MCP工具清单

### 论文解析
| 工具名 | 用途 |
|--------|------|
| `parse_papers` | 提取论文原始文本 |
| `extract_figures` | 提取图表 |

### SVG引擎
| 工具名 | 用途 |
|--------|------|
| `generate_svg_slide` | 生成幻灯片SVG |
| `generate_svg_chart` | 生成图表SVG |
| `svg_to_pptx` | SVG转PPTX |
| `check_svg_quality` | 质量检查 |

### PPT生成
| 工具名 | 用途 |
|--------|------|
| `build_slide` | 生成单页幻灯片 |
| `generate_pptx` | 最终打包 |
| `read_pptx` | 读取PPTX状态 |
| `diff_pptx` | 对比PPTX差异 |

### 规范库
| 工具名 | 用途 |
|--------|------|
| `get_academic_style` | 学术规范 |
| `get_slide_template` | 页面模板 |
| `get_citation_format` | 引用格式 |

### 预览系统
| 工具名 | 用途 |
|--------|------|
| `generate_preview` | 生成预览 |
| `generate_preview_from_pptx` | PPTX预览 |
| `start_preview_server` | 启动WebSocket |

### 反馈系统
| 工具名 | 用途 |
|--------|------|
| `detect_modifications` | 检测修改 |
| `learn_feedback` | 学习反馈 |
| `get_feedback_patterns` | 获取反馈模式 |

### 工作空间
| 工具名 | 用途 |
|--------|------|
| `cleanup_workspace` | 清理文件 |
| `get_latest_feedback` | 获取反馈 |

## 详细文档

### 角色规范
- [Paper Analyzer](references/paper-analyzer.md)
- [Content Strategist](references/content-strategist.md)
- [Visual Designer](references/visual-designer.md)
- [SVG Generator](references/slide-builder.md)
- [Quality Reviewer](references/quality-reviewer.md)
- [Professor Reviewer](references/professor-reviewer.md)
- [Material Collector](references/material-collector.md)

### 工作流文档
- [Step 1: 论文解析](workflows/step1-paper-analysis.md)
- [Step 2: 需求收集](workflows/step2-requirements.md)
- [Step 3: 目标构建](workflows/step3-goal-construction.md)
- [Step 4: 双角色审查](workflows/step4-dual-review.md)
- [Step 5: 子Agent执行](workflows/step5-sub-agents.md)
- [Step 6-10: 制作输出](workflows/step6-10-execution.md)
- [Step 8: 逐页制作PPT](workflows/step8-slide-building.md)

### 设计规范模板
- [设计规范模板](templates/design-spec-template.md)
- [执行锁模板](templates/spec-lock-template.md)

## 使用示例

```
用户: 帮我把这篇论文做成PPT

Claude:
1. 调用 parse_papers 解析论文
2. 与用户对话收集需求
3. spawn子Agent构建goal.md
4. spawn 7个子Agent并行执行
5. 审查确认
6. 生成蓝图
7. 逐页制作PPT（SVG方式）
8. 最终打包
```
