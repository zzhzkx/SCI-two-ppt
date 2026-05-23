# sci-two-ppt Skill

将科研论文转换为专业学术PPT的工具。

## 工作流程概览

```
Step 1: 论文解析 → Step 2: 需求收集 → Step 3: 目标构建
    ↓                    ↓                    ↓
Step 4: 双角色审查 → Step 5: 子Agent执行 → Step 6-10: 制作输出
```

## 7个核心角色

1. **Paper Analyzer** (论文分析专家) - 解析论文、提取关键信息
2. **Content Strategist** (内容策略师) - 规划内容结构、分配时间
3. **Visual Designer** (视觉设计师) - 设计配色、规划布局
4. **Slide Builder** (幻灯片构建师) - 逐页生成PPT
5. **Quality Reviewer** (质量审查员) - 学术审查、视觉审查
6. **Professor Reviewer** (论文教授审查员) - 专业学术审查、成果完整性评估
7. **Material Collector** (素材搜集员) - 从学术期刊搜集PPT素材

## 详细文档

### 角色规范
- [Paper Analyzer](references/paper-analyzer.md)
- [Content Strategist](references/content-strategist.md)
- [Visual Designer](references/visual-designer.md)
- [Slide Builder](references/slide-builder.md)
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
- [Step 8: 逐页制作PPT](workflows/step8-slide-building.md) - 支持SVG和python-pptx两种方式

### 设计规范模板
- [设计规范模板](templates/design-spec-template.md)
- [执行锁模板](templates/spec-lock-template.md)

## 使用方法

用户: "帮我把这篇论文做成PPT：F:\papers\paper.pdf"

Claude 应该:
1. 按照工作流文档逐步执行
2. 每个步骤调用对应的角色规范
3. 使用子Agent并行执行任务
4. 与用户保持交互确认

## MCP 工具

| 工具名 | 用途 |
|--------|------|
| `parse_papers` | 提取论文原始文本 |
| `extract_figures` | 提取图表 |
| `build_goal` | 构建目标文档 |
| `generate_blueprint` | 生成PPT蓝图 |
| `build_slide` | 生成单页幻灯片 |
| `generate_pptx` | 最终打包 |
| `get_academic_style` | 学术规范 |
| `get_slide_template` | 页面模板 |
| `generate_svg_slide` | 生成幻灯片SVG |
| `generate_svg_chart` | 生成图表SVG |
| `svg_to_pptx` | SVG转PPTX |
| `check_svg_quality` | 质量检查 |
| `generate_preview_from_pptx` | 预览PPTX |

## 注意事项

1. **子Agent并行执行**：使用Agent工具spawn独立会话
2. **用户交互贯穿全程**：每步都需要确认
3. **设计规范一致性**：使用spec_lock确保每页符合规范
4. **素材来源规范**：引用学术期刊和专业图库
