# Step 8: 逐页制作PPT

## 概述

Step 8 负责按照蓝图逐页制作PPT，支持两种制作方式：
1. **SVG方式**：AI生成SVG代码 → 浏览器预览 → 确认后转换为PPTX
2. **python-pptx方式**：直接生成PPTX文件

## 制作方式选择

### SVG方式（推荐用于复杂页面）
- **适用场景**：数据图表、技术示意图、复杂布局
- **流程**：AI生成SVG → 浏览器预览 → 用户确认 → 转换为PPTX
- **优点**：视觉效果好、可精确控制、支持复杂图表

### python-pptx方式（适用于简单页面）
- **适用场景**：纯文字页面、简单布局
- **流程**：AI生成代码 → 直接生成PPTX → 用户预览
- **优点**：快速、简单

## SVG制作流程

### 8.1 读取设计规范
```python
spec_lock = read_yaml("workspace/papers/spec_lock.md")
blueprint = read_yaml("workspace/papers/blueprint.yaml")
```

### 8.2 逐页生成SVG
```python
for slide_def in blueprint["slides"]:
    # 每页重读spec_lock（防止漂移）
    spec_lock = read_yaml("workspace/papers/spec_lock.md")
    
    # 判断使用SVG还是python-pptx
    if needs_svg(slide_def):
        # 生成SVG代码
        svg_content = generate_svg(slide_def, spec_lock)
        
        # 保存SVG文件
        svg_path = save_svg(svg_content, slide_def["index"])
        
        # 浏览器预览
        preview_url = open_in_browser(svg_path)
        
        # 等待用户确认
        user_feedback = wait_for_confirmation()
        
        if user_feedback.confirmed:
            # 转换为PPTX
            pptx_path = svg_to_pptx(svg_path)
        else:
            # 根据反馈修改SVG
            svg_content = modify_svg(svg_content, user_feedback)
            # 重新走流程
    else:
        # 使用python-pptx直接生成
        pptx_path = build_slide_python(slide_def, spec_lock)
```

### 8.3 SVG生成规范
- **画布尺寸**：1280×720像素（PPT 16:9）
- **颜色方案**：使用spec_lock中的配色
- **字体规范**：Arial/Cambria Math
- **坐标系统**：像素坐标

### 8.4 浏览器预览
- 生成HTML文件嵌入SVG
- 用户在浏览器中查看效果
- 支持缩放、平移等交互

### 8.5 用户确认流程
```
SVG生成 → 浏览器预览 → 用户查看
    ↓
用户确认 → 转换为PPTX
用户修改 → 修改SVG → 重新预览
用户跳过 → 标记为待处理
```

## python-pptx制作流程

### 8.6 直接生成PPTX
```python
for slide_def in blueprint["slides"]:
    if not needs_svg(slide_def):
        # 使用python-pptx生成
        pptx_path = build_slide_python(slide_def, spec_lock)
        
        # 生成HTML预览
        html_path = generate_preview_from_pptx(pptx_path)
        
        # 用户确认
        user_feedback = wait_for_confirmation()
```

## SVG适用场景判断

### 需要SVG的场景
- ✅ 数据图表（柱状图、折线图、饼图）
- ✅ 技术示意图（系统架构、流程图）
- ✅ 复杂布局（多栏、图文混排）
- ✅ 需要精确控制的元素

### 不需要SVG的场景
- ❌ 纯文字页面
- ❌ 简单布局
- ❌ 使用模板即可满足

## 修改反馈循环

### SVG修改
```
用户反馈修改意见
    ↓
修改SVG代码
    ↓
重新生成SVG
    ↓
浏览器预览
    ↓
用户确认
```

### PPTX修改
```
用户在PowerPoint中修改
    ↓
检测修改（diff_pptx）
    ↓
学习反馈模式
    ↓
应用到后续页面
```

## 输出文件

### SVG方式输出
- `workspace/preview/slide_*.svg` - SVG源文件
- `workspace/preview/slide_*.pptx` - 转换后的PPTX
- `workspace/preview/slide_*.html` - 浏览器预览

### python-pptx方式输出
- `workspace/preview/slide_*.pptx` - 直接生成的PPTX
- `workspace/preview/slide_*.html` - HTML预览

## 质量检查

### SVG质量检查
```python
# 转换前检查SVG质量
quality_result = check_svg_quality(svg_content)
if not quality_result["passed"]:
    # 修正SVG
    fix_svg_issues(svg_content, quality_result["errors"])
```

### PPTX质量检查
```python
# 生成后检查PPTX
pptx_result = check_pptx_quality(pptx_path)
if not pptx_result["passed"]:
    # 修正PPTX
    fix_pptx_issues(pptx_path, pptx_result["errors"])
```

## 完整流程图

```
Step 8: 逐页制作PPT

读取蓝图和spec_lock
        ↓
    ┌───────────────┐
    │ 逐页循环       │
    └───────┬───────┘
            ↓
    ┌───────────────┐
    │ 判断制作方式   │
    └───────┬───────┘
            ↓
    ┌───────┴───────┐
    ↓               ↓
SVG方式          python-pptx方式
    ↓               ↓
生成SVG          生成PPTX
    ↓               ↓
浏览器预览       HTML预览
    ↓               ↓
用户确认         用户确认
    ↓               ↓
SVG转PPTX        保留PPTX
    ↓               ↓
    └───────┬───────┘
            ↓
    ┌───────────────┐
    │ 下一页         │
    └───────────────┘
```
