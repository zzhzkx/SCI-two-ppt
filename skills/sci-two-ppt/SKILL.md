# sci-two-ppt Skill

将科研论文转换为专业学术PPT的工具。

## 核心架构

```
Claude Code (大脑) → 生成SVG代码 → MCP工具转换 → PPTX输出
```

**SVG引擎**：基于PPT Master的SVG转PPTX方案
- AI生成SVG（自然、灵活、可预览）
- SVG后处理（图标嵌入、文本展平、圆角转路径）
- 质量检查（禁止元素、字体安全、规范符合）
- 转换为PPTX（可编辑）

## 10步工作流（SVG版本）

### Step 1: 论文解析
- 调用 `parse_papers` 提取原始文本
- spawn子Agent智能分析论文
- 生成检索式

### Step 2: 需求收集
- 智能推荐PPT用途
- 分层询问需求

### Step 3: 目标构建
- spawn子Agent构建goal.md

### Step 4: 双角色审查
- 领域专家审查
- PPT制作师审查

### Step 5: 子Agent生成SVG代码
**关键步骤** - 并行执行多个子Agent：

```
Agent 1: 封面SVG生成
- 输入：论文标题、作者、单位
- 输出：workspace/preview/slide_0.svg

Agent 2: 内容页SVG生成
- 输入：各章节内容
- 输出：workspace/preview/slide_1.svg ~ slide_N.svg

Agent 3: 数据图表SVG生成
- 输入：实验数据、误差分析
- 输出：workspace/preview/chart_*.svg

Agent 4: 技术示意图SVG生成
- 输入：系统架构、光路设计
- 输出：workspace/preview/diagram_*.svg

Agent 5: 学术内容SVG生成
- 输入：公式、变量说明
- 输出：workspace/preview/formula_*.svg
```

**SVG代码规范**：
- 画布：1280×720像素（PPT 16:9）
- 颜色：使用spec_lock中的配色方案
- 字体：Arial/Cambria Math
- 坐标：像素坐标系统

### Step 6: SVG后处理 + 质量检查
```
1. finalize_svg: 嵌入图标、展平文本、圆角转路径
2. svg_quality_checker: 检查禁止元素、字体安全、规范符合
3. 如果检查失败，返回Step 5修正
```

### Step 7: SVG转PPTX
- 调用 `svg_to_pptx` 批量转换所有SVG
- 输出：workspace/output/slide_*.pptx

### Step 8: 逐页预览确认
- 生成HTML预览（从PPTX读取，保持一致）
- 用户在浏览器查看
- 提出修改意见
- 如果需要修改，返回Step 5重新生成SVG

### Step 9: 最终打包
- 合并所有幻灯片
- 生成最终PPTX

### Step 10: 整理文件
- 清理中间文件
- 保留最终产出

## MCP工具清单

### SVG生成工具
| 工具名 | 用途 |
|--------|------|
| `generate_svg_slide` | 生成幻灯片SVG |
| `generate_svg_chart` | 生成图表SVG |

### SVG处理工具
| 工具名 | 用途 |
|--------|------|
| `svg_to_pptx` | SVG转PPTX |
| `check_svg_quality` | 质量检查 |

### 其他工具
| 工具名 | 用途 |
|--------|------|
| `parse_papers` | 解析论文 |
| `build_goal` | 构建目标文档 |
| `generate_preview_from_pptx` | 预览PPTX |

## 角色系统

1. **Paper Analyzer** (论文分析专家) - 解析论文、提取关键信息
2. **Content Strategist** (内容策略师) - 规划内容结构、分配时间
3. **Visual Designer** (视觉设计师) - 设计配色、规划布局
4. **SVG Generator** (SVG生成器) - 生成SVG代码
5. **Quality Reviewer** (质量审查员) - 学术审查、视觉审查
6. **Professor Reviewer** (论文教授审查员) - 专业学术审查
7. **Material Collector** (素材搜集员) - 搜集图表素材

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

### 设计规范模板
- [设计规范模板](templates/design-spec-template.md)
- [执行锁模板](templates/spec-lock-template.md)

## SVG代码模板

### 封面页
```svg
<svg viewBox="0 0 1280 720">
  <defs>
    <linearGradient id="bg">...</linearGradient>
  </defs>
  <rect fill="url(#bg)" width="1280" height="720"/>
  <text x="640" y="300" text-anchor="middle" font-size="48">标题</text>
  <text x="640" y="400" text-anchor="middle" font-size="28">副标题</text>
</svg>
```

### 柱状图
```svg
<svg viewBox="0 0 1280 720">
  <rect fill="white" width="1280" height="720"/>
  <text x="640" y="50" text-anchor="middle" font-size="28">图表标题</text>
  <rect x="150" y="200" width="80" height="400" fill="#1B6CA8"/>
  <!-- 更多柱子... -->
</svg>
```

## 注意事项

1. **SVG规范**：必须符合PPT Master的SVG规范
2. **坐标系统**：使用1280×720像素画布
3. **颜色方案**：使用spec_lock中的配色
4. **字体安全**：使用PPT预装字体
5. **质量检查**：转换前必须通过质量检查
6. **子Agent并行执行**：使用Agent工具spawn独立会话
7. **用户交互贯穿全程**：每步都需要确认
