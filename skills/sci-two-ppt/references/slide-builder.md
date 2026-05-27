# Slide Builder (幻灯片构建师) 规范

## 角色定位

幻灯片构建师负责根据设计规范和内容规划，逐页生成PPT幻灯片，确保每页符合视觉规范和内容要求。

## 职责范围

### 核心职责
1. 读取设计规范（spec_lock.md）
2. 读取PPT蓝图（blueprint.yaml）
3. 逐页生成幻灯片
4. 应用视觉规范
5. 生成预览文件

### 输入
- `workspace/blueprint.yaml` - PPT蓝图
- `workspace/papers/spec_lock.md` - 视觉规范（如已生成）
- `workspace/materials/` - 素材资源

### 输出
- `workspace/preview/slide_*.pptx` - 单页幻灯片
- `workspace/output/output_final.pptx` - 最终PPT

## 工作流程

### Step 1: 读取设计规范
```python
# 每页构建前必须读取spec_lock
spec_lock = read_yaml("workspace/papers/spec_lock.md")

# 提取关键规范
colors = spec_lock["colors"]
fonts = spec_lock["fonts"]
layouts = spec_lock["layouts"]
```

### Step 2: 读取PPT蓝图
```python
# 读取蓝图
blueprint = read_yaml("workspace/blueprint.yaml")

# 获取每页定义
slides = blueprint["slides"]
```

### Step 3: 逐页生成幻灯片
```python
for slide_def in slides:
    # 读取spec_lock（防止上下文压缩导致的漂移）
    spec_lock = read_yaml("workspace/papers/spec_lock.md")
    
    # 生成单页
    slide = build_single_slide(slide_def, spec_lock)
    
    # 保存预览
    save_preview(slide, slide_def["index"])
```

### Step 4: 应用视觉规范
```python
def build_single_slide(slide_def, spec_lock):
    # 创建幻灯片
    slide = Presentation().slides.add_slide()
    
    # 应用颜色规范
    apply_colors(slide, spec_lock["colors"])
    
    # 应用字体规范
    apply_fonts(slide, spec_lock["fonts"])
    
    # 应用布局规范
    apply_layout(slide, slide_def["type"], spec_lock["layouts"])
    
    # 添加内容
    add_content(slide, slide_def)
    
    return slide
```

### Step 5: 生成预览文件
```python
# 保存为PPTX
slide.save(f"workspace/preview/slide_{index}.pptx")

# 生成HTML预览（可选）
generate_html_preview(slide, index)
```

## 幻灯片类型

### 1. 封面页 (title_slide)
```python
def build_title_slide(slide_def, spec_lock):
    # 标题
    title = add_textbox(
        text=slide_def["title"],
        position="center",
        font=spec_lock["fonts"]["title"]
    )
    
    # 副标题
    subtitle = add_textbox(
        text=slide_def["subtitle"],
        position="below_title",
        font=spec_lock["fonts"]["subtitle"]
    )
    
    # 背景
    apply_background(slide, "gradient", spec_lock["colors"])
```

### 2. 内容页 (content_slide)
```python
def build_content_slide(slide_def, spec_lock):
    # 标题栏
    title = add_textbox(
        text=slide_def["title"],
        position="top",
        font=spec_lock["fonts"]["title"]
    )
    
    # 内容区域
    content = add_textbox(
        text=slide_def["content"],
        position="left",
        font=spec_lock["fonts"]["body"]
    )
    
    # 图表区域（如有）
    if "figure" in slide_def:
        figure = add_figure(
            path=slide_def["figure"],
            position="right"
        )
```

### 3. 图表页 (chart_slide)
```python
def build_chart_slide(slide_def, spec_lock):
    # 标题
    title = add_textbox(
        text=slide_def["title"],
        position="top",
        font=spec_lock["fonts"]["title"]
    )
    
    # 图表
    chart = add_chart(
        data=slide_def["chart_data"],
        style=spec_lock["charts"]["style"],
        colors=spec_lock["charts"]["colors"]
    )
    
    # 图注
    caption = add_textbox(
        text=slide_def["caption"],
        position="below_chart",
        font=spec_lock["fonts"]["caption"]
    )
```

### 4. 总结页 (conclusion_slide)
```python
def build_conclusion_slide(slide_def, spec_lock):
    # 标题
    title = add_textbox(
        text=slide_def["title"],
        position="center",
        font=spec_lock["fonts"]["title"]
    )
    
    # 内容
    content = add_textbox(
        text=slide_def["content"],
        position="center",
        font=spec_lock["fonts"]["body"]
    )
    
    # 背景
    apply_background(slide, "solid", spec_lock["colors"])
```

## 视觉规范应用

### 颜色应用
```python
def apply_colors(slide, colors):
    # 背景色
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = colors["background"]
    
    # 标题颜色
    for shape in slide.shapes:
        if shape.has_text_frame:
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    run.font.color.rgb = colors["text_primary"]
```

### 字体应用
```python
def apply_fonts(slide, fonts):
    for shape in slide.shapes:
        if shape.has_text_frame:
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    # 根据文本类型应用字体
                    if is_title(run.text):
                        run.font.name = fonts["title"]["family"]
                        run.font.size = Pt(fonts["title"]["size"])
                        run.font.bold = True
                    else:
                        run.font.name = fonts["body"]["family"]
                        run.font.size = Pt(fonts["body"]["size"])
```

### 布局应用
```python
def apply_layout(slide, slide_type, layouts):
    layout = layouts[slide_type]
    
    # 设置边距
    slide.left = Inches(layout.get("margin_left", 1))
    slide.top = Inches(layout.get("margin_top", 1))
    slide.width = Inches(layout.get("width", 13.333))
    slide.height = Inches(layout.get("height", 7.5))
```

## 输出格式

### 单页幻灯片
- 文件：`workspace/preview/slide_{index}.pptx`
- 格式：PowerPoint 2007+
- 尺寸：16:9 宽屏

### 最终PPT
- 文件：`workspace/output/output_final.pptx`
- 包含所有确认的幻灯片
- 应用统一的视觉规范

## 质量检查

### 每页检查
- ✅ 颜色符合spec_lock
- ✅ 字体符合spec_lock
- ✅ 布局符合规范
- ✅ 内容完整准确
- ✅ 图片清晰可见

### 整体检查
- ✅ 风格一致性
- ✅ 逻辑连贯性
- ✅ 时间合理性
- ✅ 视觉舒适度

## 与其他角色的协作

### 上游
- 接收 Visual Designer 的 spec_lock.md
- 接收 Content Strategist 的 blueprint.yaml
- 接收 Material Collector 的素材

### 下游
- 向 Quality Reviewer 提供生成的幻灯片
- 向用户提供预览文件

## 最佳实践

1. **每页重读spec_lock**：防止上下文压缩导致的漂移
2. **逐页生成**：避免批量生成导致的问题
3. **视觉一致性**：确保所有页面风格统一
4. **内容准确性**：确保内容与蓝图一致
5. **预览及时**：每页生成后立即提供预览
