# sci-two-ppt Skill

将科研论文转换为专业学术PPT的工具。

## 工作流程概览

```
Step 1: 论文解析 → Step 2: 需求收集 → Step 3: 目标构建
    ↓                    ↓                    ↓
Step 4: 双角色审查 → Step 5: 子Agent执行 → Step 6-10: 制作输出
```

## 7个核心角色

1. Paper Analyzer - 论文分析专家
2. Content Strategist - 内容策略师
3. Visual Designer - 视觉设计师
4. Slide Builder - 幻灯片构建师
5. Quality Reviewer - 质量审查员
6. Professor Reviewer - 论文教授审查员
7. Material Collector - 素材搜集员

## MCP 工具

| 工具名 | 用途 |
|--------|------|
| parse_papers | 提取论文原始文本 |
| extract_figures | 提取图表 |
| build_goal | 构建目标文档 |
| generate_blueprint | 生成PPT蓝图 |
| build_slide | 生成单页幻灯片 |
| generate_pptx | 最终打包 |
| get_academic_style | 学术规范 |
| get_slide_template | 页面模板 |
| generate_svg_slide | 生成幻灯片SVG |
| generate_svg_chart | 生成图表SVG |
| svg_to_pptx | SVG转PPTX |
| check_svg_quality | 质量检查 |
| generate_preview_from_pptx | 预览PPTX |

## Step 8: 逐页制作PPT

支持两种方式：
1. SVG方式：AI生成SVG → 浏览器预览 → 确认 → 转换PPTX
2. python-pptx方式：直接生成PPTX

详见 [Step 8工作流](workflows/step8-slide-building.md)
