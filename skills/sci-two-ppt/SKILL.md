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

### Step 1-4: 需求分析（不变）

### Step 5: 子Agent生成SVG代码
关键步骤 - 并行执行多个子Agent：
- Agent 1: 封面SVG
- Agent 2: 内容页SVG
- Agent 3: 数据图表SVG
- Agent 4: 技术示意图SVG
- Agent 5: 学术内容SVG

### Step 6: SVG后处理 + 质量检查
- finalize_svg: 嵌入图标、展平文本
- svg_quality_checker: 质量检查

### Step 7: SVG转PPTX
- svg_to_pptx: 批量转换

### Step 8-10: 预览、确认、打包

## MCP工具

| 工具名 | 用途 |
|--------|------|
| generate_svg_slide | 生成幻灯片SVG |
| generate_svg_chart | 生成图表SVG |
| svg_to_pptx | SVG转PPTX |
| check_svg_quality | 质量检查 |
| parse_papers | 解析论文 |
| generate_preview_from_pptx | 预览PPTX |

## SVG规范

- 画布：1280x720像素
- 坐标：像素坐标系统
- 字体：Arial/Cambria Math
- 颜色：使用spec_lock配色
