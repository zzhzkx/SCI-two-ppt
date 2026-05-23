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
