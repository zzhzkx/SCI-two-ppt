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
**审核内容**：论文解析结果
- 标题、摘要、方法、结果是否准确
- 关键发现和创新点是否完整
- 检索式是否合理

**用户确认后**：进入Step 2

### Step 2 完成后
**审核内容**：需求文档
- PPT用途、时长、听众是否正确
- 风格偏好是否明确
- 重点内容是否清晰

**用户确认后**：进入Step 3

### Step 3 完成后
**审核内容**：目标文档
- 章节结构是否合理
- 时间分配是否合适
- 核心要点是否突出

**用户确认后**：进入Step 4

### Step 4 完成后
**审核内容**：审查报告
- 领域专家审查建议
- PPT制作师审查建议
- 需要修改的部分

**用户确认后**：进入Step 5

### Step 5 完成后
**审核内容**：所有Agent产出
- 论文要点是否准确
- 创新点是否突出
- UI设计是否满意
- 章节结构是否合理
- 讲解备注是否完整

**用户确认后**：进入Step 6

### Step 6 完成后
**审核内容**：最终确认
- 所有内容是否满意
- 是否需要补充或修改

**用户确认后**：进入Step 7

### Step 7 完成后
**审核内容**：PPT蓝图
- 每页内容是否完整
- 时间分配是否合理
- 布局是否合适

**用户确认后**：进入Step 8

### Step 8 完成后
**审核内容**：每一页PPT
- 内容是否准确
- 视觉效果是否满意
- 是否需要修改

**用户确认后**：进入Step 9

### Step 9 完成后
**审核内容**：最终PPT
- 整体效果是否满意
- 是否需要调整

**用户确认后**：进入Step 10

### Step 10 完成后
**审核内容**：最终产出
- PPT文件是否完整
- 制作报告是否详细

**用户确认后**：流程完成

## 7个核心角色（对应 run_subagent 的 agent_type）

| 角色 | agent_type | 职责 | 输入 | 输出文件 |
|------|-----------|------|------|----------|
| Paper Analyzer | `paper_keypoints` | 论文要点提取 | analysis.json | 01_paper_keypoints.md |
| Content Strategist | `innovation_points` | 创新点提炼 | 01_paper_keypoints.md | 02_innovation_points.md |
| Paper Analyzer | `simulation_code` | 仿真代码分析 | analysis.json | 03_simulation_code.md |
| Material Collector | `visual_resources` | 学术配图搜集 | analysis.json + search_queries.json | 04_visual_resources.md |
| Visual Designer | `ui_design` | UI风格设计 | goal.md | 05_ui_design.md |
| Content Strategist | `chapter_structure` | 章节结构安排 | 01 + 02 | 06_chapter_structure.md |
| Content Strategist | `speaker_notes` | 讲解备注 | 06_chapter_structure.md | 07_speaker_notes.md |

**并行关系**：Agent 1~4 可并行；Agent 5 依赖 Agent1；Agent 6 依赖 Agent1+2；Agent 7 依赖 Agent6

## MCP工具清单（25个工具）

### 论文解析（2个）
| 工具名 | 用途 |
|--------|------|
| `parse_papers` | 提取论文原始文本（PDF/Word） |
| `extract_figures` | 提取PDF中的图表和图片 |

### 内容规划（2个）
| 工具名 | 用途 |
|--------|------|
| `build_goal` | 构建结构化PPT目标文档 |
| `run_subagent` | 执行7种类型的子Agent任务 |

### SVG引擎（4个）
| 工具名 | 用途 |
|--------|------|
| `generate_svg_slide` | 生成幻灯片SVG |
| `generate_svg_chart` | 生成图表SVG |
| `svg_to_pptx` | SVG转PPTX |
| `check_svg_quality` | SVG质量检查 |

### PPT生成（5个）
| 工具名 | 用途 |
|--------|------|
| `build_slide` | 生成单页幻灯片 |
| `generate_blueprint` | 生成PPT蓝图YAML |
| `generate_pptx` | 最终打包生成PPTX |
| `read_pptx` | 读取PPTX状态 |
| `diff_pptx` | 对比PPTX差异 |

### 规范库（3个）
| 工具名 | 用途 |
|--------|------|
| `get_academic_style` | 学术规范（配色/字体/排版） |
| `get_slide_template` | 页面模板 |
| `get_citation_format` | 引用格式 |

### 预览系统（4个）
| 工具名 | 用途 |
|--------|------|
| `generate_preview` | 从蓝图数据生成HTML预览 |
| `generate_preview_from_pptx` | 从PPTX文件生成HTML预览 |
| `render_preview` | 渲染幻灯片为预览图片 |
| `start_preview_server` | 启动WebSocket预览服务器 |

### 反馈系统（3个）
| 工具名 | 用途 |
|--------|------|
| `detect_modifications` | 检测PPTX文件修改 |
| `learn_feedback` | 从用户修改学习反馈模式 |
| `get_feedback_patterns` | 获取已积累的反馈模式 |

### 工作空间（2个）
| 工具名 | 用途 |
|--------|------|
| `cleanup_workspace` | 整理清理工作空间 |
| `get_latest_feedback` | 获取最新用户反馈 |

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
