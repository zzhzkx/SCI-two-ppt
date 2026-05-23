# Step 8: 逐页制作PPT

## 概述

Step 8 负责按照蓝图逐页制作PPT，支持两种制作方式：
1. **SVG方式**：AI生成SVG代码 → 浏览器预览 → 确认后转换为PPTX
2. **python-pptx方式**：直接生成PPTX文件

## 制作方式选择

### SVG方式（推荐用于复杂页面）
- 适用场景：数据图表、技术示意图、复杂布局
- 流程：AI生成SVG → 浏览器预览 → 用户确认 → 转换为PPTX
- 优点：视觉效果好、可精确控制、支持复杂图表

### python-pptx方式（适用于简单页面）
- 适用场景：纯文字页面、简单布局
- 流程：AI生成代码 → 直接生成PPTX → 用户预览
- 优点：快速、简单

## SVG制作流程

### 8.1 读取设计规范
```python
spec_lock = read_yaml("workspace/papers/spec_lock.md")
blueprint = read_yaml("workspace/papers/blueprint.yaml")
```

### 8.2 逐页生成SVG
```python
for slide_def in blueprint["slides"]:
    if needs_svg(slide_def):
        svg_content = generate_svg(slide_def, spec_lock)
        svg_path = save_svg(svg_content, slide_def["index"])
        preview_url = open_in_browser(svg_path)
        user_feedback = wait_for_confirmation()
        
        if user_feedback.confirmed:
            pptx_path = svg_to_pptx(svg_path)
```

### 8.3 SVG生成规范
- 画布尺寸：1280×720像素（PPT 16:9）
- 颜色方案：使用spec_lock中的配色
- 字体规范：Arial/Cambria Math
- 坐标系统：像素坐标

## 完整流程图

```
Step 8: 逐页制作PPT

读取蓝图和spec_lock
        ↓
    逐页循环
        ↓
    判断制作方式
        ↓
    SVG方式 或 python-pptx方式
        ↓
    生成SVG/PPTX
        ↓
    浏览器预览/HTML预览
        ↓
    用户确认
        ↓
    下一页
```
