# Step 6-10: 制作输出工作流

## 概述

Step 6-10 负责审查确认、生成蓝图、逐页制作、最终打包和文件整理。

## 角色

- **Quality Reviewer** (质量审查员) - 最终审查
- **Slide Builder** (幻灯片构建师) - 逐页构建

## Step 6: 审查与确认

### 6.1 读取所有Agent产出
```python
agent_results = read_directory("workspace/agent_results/")
```

### 6.2 展示结果摘要
向用户展示：
- 论文要点
- 创新点
- UI设计
- 章节结构
- 讲解备注

### 6.3 用户确认
- 用户确认或要求修改
- 如果需要修改，返回Step 5重新执行相关Agent

## Step 7: 生成PPT蓝图

### 7.1 综合所有信息
```python
goal = read_file("workspace/goal.md")
agent_results = read_directory("workspace/agent_results/")
ui_design = read_file("workspace/agent_results/05_ui_design.md")
chapter_structure = read_file("workspace/agent_results/06_chapter_structure.md")
```

### 7.2 生成蓝图
```python
blueprint = {
    "slides": [
        {
            "index": 0,
            "type": "title",
            "title": "论文标题",
            "subtitle": "作者信息",
            "notes": "开场白",
            "duration_seconds": 30
        },
        # ... 更多页面
    ]
}
```

### 7.3 保存蓝图
保存到 `workspace/papers/blueprint.yaml`

## Step 8: 逐页制作PPT

### 8.1 读取设计规范
```python
spec_lock = read_yaml("workspace/papers/spec_lock.md")
blueprint = read_yaml("workspace/papers/blueprint.yaml")
```

### 8.2 预览方式

#### 方式1：HTML预览（推荐）
```python
def generate_html_preview(slide, index):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Slide {index} Preview</title>
        <style>
            body {{ font-family: Arial; margin: 20px; }}
            .slide {{ border: 1px solid #ccc; padding: 20px; }}
            .controls {{ margin-top: 20px; }}
            button {{ margin-right: 10px; padding: 10px 20px; }}
        </style>
    </head>
    <body>
        <h1>Slide {index} Preview</h1>
        <div class="slide">
            {render_slide_html(slide)}
        </div>
        <div class="controls">
            <button onclick="confirm()">✅ 确认</button>
            <button onclick="modify()">✏️ 修改</button>
            <button onclick="skip()">⏭️ 跳过</button>
            <button onclick="redo()">🔄 重做</button>
        </div>
        <div class="feedback">
            <textarea id="feedback" placeholder="输入修改意见..."></textarea>
            <button onclick="submitFeedback()">提交意见</button>
        </div>
    </body>
    </html>
    """
    save_file(f"workspace/preview/slide_{index}.html", html)
    return f"workspace/preview/slide_{index}.html"
```

#### 方式2：图片预览
```python
def generate_image_preview(slide, index):
    image_path = f"workspace/preview/slide_{index}.png"
    render_slide_to_image(slide, image_path)
    return image_path
```

#### 方式3：直接打开PPT
```python
def open_in_powerpoint(pptx_path):
    import subprocess
    subprocess.Popen(["start", pptx_path], shell=True)
```

### 8.3 修改方式

#### 方式1：对话式修改
```python
user_feedback = {
    "type": "modify",
    "content": "标题字号太小，改成40pt",
    "target": "title",
    "property": "font_size",
    "value": 40
}
```

#### 方式2：标注式修改
```python
user_feedback = {
    "type": "annotate",
    "annotations": [
        {"x": 100, "y": 200, "comment": "这里需要加图片"},
        {"x": 300, "y": 400, "comment": "颜色太浅"}
    ]
}
```

#### 方式3：手动修改后反馈
```python
user_feedback = {
    "type": "manual_edit",
    "original": "workspace/preview/slide_1.pptx",
    "modified": "workspace/preview/slide_1_modified.pptx",
    "changes": detect_changes(original, modified)
}
```

### 8.4 逐页生成与审查循环
```python
for slide_def in blueprint["slides"]:
    # 每页重读spec_lock（防止漂移）
    spec_lock = read_yaml("workspace/papers/spec_lock.md")
    
    # 生成单页
    slide = build_slide(slide_def, spec_lock)
    
    # 保存预览（多种格式）
    save_preview(slide, slide_def["index"], formats=["html", "png", "pptx"])
    
    # 提供预览
    preview_path = generate_html_preview(slide, slide_def["index"])
    show_preview_to_user(preview_path)
    
    # 等待用户审查
    user_feedback = wait_for_user_review()
    
    # 处理用户意见
    while user_feedback:
        if user_feedback.type == "confirm":
            break
        elif user_feedback.type == "modify":
            slide = modify_slide(slide, user_feedback.content)
            save_preview(slide, slide_def["index"])
            show_preview_to_user(slide)
            user_feedback = wait_for_user_review()
        elif user_feedback.type == "manual_edit":
            # 检测用户手动修改
            changes = detect_changes(user_feedback.original, user_feedback.modified)
            # 学习反馈模式
            feedback_patterns = learn_from_feedback(changes, slide_def["index"])
            # 应用修改
            slide = apply_changes(slide, changes)
            save_preview(slide, slide_def["index"])
            show_preview_to_user(slide)
            user_feedback = wait_for_user_review()
        elif user_feedback.type == "skip":
            mark_as_pending(slide_def["index"])
            break
        elif user_feedback.type == "redo":
            slide = build_slide(slide_def, spec_lock)
            save_preview(slide, slide_def["index"])
            show_preview_to_user(slide)
            user_feedback = wait_for_user_review()
    
    # 记录修改历史
    record_modification_history(slide_def["index"], user_feedback)
```

### 8.5 手动修改反馈学习

#### 检测变化
```python
def detect_changes(original_path, modified_path):
    """检测用户在PowerPoint中的手动修改"""
    from pptx import Presentation
    
    original = Presentation(original_path)
    modified = Presentation(modified_path)
    
    changes = []
    
    for orig_slide, mod_slide in zip(original.slides, modified.slides):
        for orig_shape, mod_shape in zip(orig_slide.shapes, mod_slide.shapes):
            # 检测文本变化
            if orig_shape.has_text_frame and mod_shape.has_text_frame:
                if orig_shape.text != mod_shape.text:
                    changes.append({
                        "type": "text",
                        "shape": orig_shape.name,
                        "original": orig_shape.text,
                        "modified": mod_shape.text
                    })
            
            # 检测位置变化
            if (orig_shape.left != mod_shape.left or 
                orig_shape.top != mod_shape.top):
                changes.append({
                    "type": "position",
                    "shape": orig_shape.name,
                    "original": {"left": orig_shape.left, "top": orig_shape.top},
                    "modified": {"left": mod_shape.left, "top": mod_shape.top}
                })
            
            # 检测大小变化
            if (orig_shape.width != mod_shape.width or 
                orig_shape.height != mod_shape.height):
                changes.append({
                    "type": "size",
                    "shape": orig_shape.name,
                    "original": {"width": orig_shape.width, "height": orig_shape.height},
                    "modified": {"width": mod_shape.width, "height": mod_shape.height}
                })
    
    return changes
```

#### 学习反馈模式
```python
def learn_from_feedback(changes, slide_index):
    """从用户修改中学习反馈模式"""
    
    feedback_patterns = {
        "font_size_changes": [],
        "position_adjustments": [],
        "color_changes": [],
        "text_rewrites": []
    }
    
    for change in changes:
        if change["type"] == "text":
            feedback_patterns["text_rewrites"].append({
                "original": change["original"],
                "modified": change["modified"],
                "slide": slide_index
            })
        elif change["type"] == "position":
            feedback_patterns["position_adjustments"].append({
                "shape": change["shape"],
                "dx": change["modified"]["left"] - change["original"]["left"],
                "dy": change["modified"]["top"] - change["original"]["top"],
                "slide": slide_index
            })
        elif change["type"] == "size":
            feedback_patterns["font_size_changes"].append({
                "shape": change["shape"],
                "dw": change["modified"]["width"] - change["original"]["width"],
                "dh": change["modified"]["height"] - change["original"]["height"],
                "slide": slide_index
            })
    
    return feedback_patterns
```

#### 生成反馈总结
```python
def generate_feedback_summary(feedback_patterns):
    """生成反馈总结，应用到后续页面"""
    
    summary = """
    # 用户反馈总结
    
    ## 修改模式分析
    
    ### 文本修改
    {text_changes}
    
    ### 位置调整
    {position_changes}
    
    ### 大小调整
    {size_changes}
    
    ## 应用建议
    
    基于以上修改模式，建议后续页面：
    1. {suggestion_1}
    2. {suggestion_2}
    3. {suggestion_3}
    """.format(**feedback_patterns)
    
    return summary
```

#### 应用反馈到后续页面
```python
def apply_feedback_to_next_slides(feedback_patterns, blueprint):
    """将反馈应用到后续页面"""
    
    for slide_def in blueprint["slides"]:
        # 应用字体大小调整
        for change in feedback_patterns["font_size_changes"]:
            if slide_def["index"] > change["slide"]:
                apply_size_adjustment(slide_def, change)
        
        # 应用位置调整
        for change in feedback_patterns["position_adjustments"]:
            if slide_def["index"] > change["slide"]:
                apply_position_adjustment(slide_def, change)
    
    return blueprint
```

### 8.6 用户审查交互
- **每页完成后立即交给用户审查**
- **用户可以随时提出意见**：
  - ✅ 确认：这页OK，继续下一页
  - ✏️ 修改：提出具体修改意见
  - ⏭️ 跳过：暂时跳过，稍后处理
  - 🔄 重做：完全重新设计这页
  - 💬 意见：提出任何意见和建议

### 8.7 审查要点
用户审查时可以关注：
- **内容准确性**：文字、数据、公式是否正确
- **视觉效果**：配色、布局、字体是否美观
- **逻辑流畅**：与前后页是否衔接自然
- **重点突出**：创新点是否突出展示
- **时间合理**：内容量是否适合分配的时间

### 8.8 修改记录
```python
modification_history = {
    "slide_1": [
        {"action": "modify", "content": "标题字号太小", "timestamp": "..."},
        {"action": "confirm", "timestamp": "..."}
    ],
    "slide_2": [
        {"action": "manual_edit", "changes": [...], "timestamp": "..."},
        {"action": "confirm", "timestamp": "..."}
    ]
}
```

### 8.9 跳过页面处理
```python
pending_slides = get_pending_slides()

if pending_slides:
    print("还有以下页面未确认：")
    for slide in pending_slides:
        print(f"  - 第{slide.index}页: {slide.title}")
    
    for slide in pending_slides:
        show_preview_to_user(slide)
        user_feedback = wait_for_user_review()
        # ... 处理用户意见
```

### 8.10 反馈学习应用
```python
# 在所有页面完成后，生成反馈总结
feedback_summary = generate_feedback_summary(feedback_patterns)
save_file("workspace/feedback/feedback_summary.md", feedback_summary)

# 将反馈应用到未来项目
save_feedback_patterns(feedback_patterns, "workspace/feedback/feedback_patterns.json")
```

## Step 9: 生成最终PPT

### 9.1 合并所有幻灯片
```python
final_ppt = merge_slides(confirmed_slides)
```

### 9.2 应用统一规范
```python
apply_spec_lock(final_ppt, spec_lock)
```

### 9.3 保存最终PPT
保存到 `workspace/output/output_final.pptx`

## Step 10: 整理文件

### 10.1 生成制作报告
```python
report = generate_production_report(
    goal=goal,
    agent_results=agent_results,
    blueprint=blueprint,
    final_ppt=final_ppt
)
save_file("workspace/production_report.md", report)
```

### 10.2 清理中间文件
```python
cleanup_workspace(
    keep=["output/", "papers/", "agent_results/"],
    remove=["preview/", "temp/"]
)
```

### 10.3 整理最终产出
```
workspace/
├── output/
│   └── output_final.pptx    # 最终PPT
├── papers/
│   ├── analysis.json        # 论文分析
│   ├── goal.md              # 目标文档
│   ├── blueprint.yaml       # PPT蓝图
│   └── spec_lock.md         # 设计规范
├── agent_results/           # Agent产出
├── materials/               # 素材资源
└── production_report.md     # 制作报告
```

## 输出文件

### 最终产出
- `workspace/output/output_final.pptx` - 最终PPT文件

### 过程文档
- `workspace/production_report.md` - 制作报告
- `workspace/papers/` - 论文分析和目标文档
- `workspace/agent_results/` - Agent产出
- `workspace/materials/` - 素材资源

## 质量检查

### 最终检查
- ✅ 文件可正常打开
- ✅ 字体正确嵌入
- ✅ 图片清晰可见
- ✅ 动画正常播放
- ✅ 内容完整准确
