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

### 8.2 逐页生成
```python
for slide_def in blueprint["slides"]:
    # 每页重读spec_lock（防止漂移）
    spec_lock = read_yaml("workspace/papers/spec_lock.md")
    
    # 生成单页
    slide = build_slide(slide_def, spec_lock)
    
    # 保存预览
    save_preview(slide, slide_def["index"])
    
    # 展示给用户审查
    show_preview_to_user(slide)
    
    # 等待用户审查和意见
    user_feedback = wait_for_user_review()
    
    # 处理用户意见
    while user_feedback:
        if user_feedback.type == "confirm":
            # 用户确认，继续下一页
            break
        elif user_feedback.type == "modify":
            # 用户提出修改意见
            slide = modify_slide(slide, user_feedback.content)
            save_preview(slide, slide_def["index"])
            show_preview_to_user(slide)
            user_feedback = wait_for_user_review()
        elif user_feedback.type == "skip":
            # 用户跳过，稍后处理
            mark_as_pending(slide_def["index"])
            break
        elif user_feedback.type == "redo":
            # 用户要求重做
            slide = build_slide(slide_def, spec_lock)
            save_preview(slide, slide_def["index"])
            show_preview_to_user(slide)
            user_feedback = wait_for_user_review()
```

### 8.3 用户审查交互
- **每页完成后立即交给用户审查**
- **用户可以随时提出意见**：
  - ✅ 确认：这页OK，继续下一页
  - ✏️ 修改：提出具体修改意见
  - ⏭️ 跳过：暂时跳过，稍后处理
  - 🔄 重做：完全重新设计这页
  - 💬 意见：提出任何意见和建议

### 8.4 意见处理循环
```
生成第N页
    ↓
展示给用户审查
    ↓
用户提出意见 ←────────────┐
    ↓                      │
根据意见修改               │
    ↓                      │
重新展示给用户审查 ─────────┘
    ↓
用户确认 → 继续第N+1页
```

### 8.5 审查要点
用户审查时可以关注：
- **内容准确性**：文字、数据、公式是否正确
- **视觉效果**：配色、布局、字体是否美观
- **逻辑流畅**：与前后页是否衔接自然
- **重点突出**：创新点是否突出展示
- **时间合理**：内容量是否适合分配的时间
- **其他意见**：任何想法和建议

### 8.6 修改记录
```python
# 记录每页的修改历史
modification_history = {
    "slide_1": [
        {"action": "modify", "content": "标题字号太小", "timestamp": "..."},
        {"action": "confirm", "timestamp": "..."}
    ],
    "slide_2": [
        {"action": "redo", "content": "重新设计布局", "timestamp": "..."},
        {"action": "modify", "content": "图片位置调整", "timestamp": "..."},
        {"action": "confirm", "timestamp": "..."}
    ]
}
```

### 8.7 跳过页面处理
```python
# 处理跳过的页面
pending_slides = get_pending_slides()

if pending_slides:
    print("还有以下页面未确认：")
    for slide in pending_slides:
        print(f"  - 第{slide.index}页: {slide.title}")
    
    # 继续处理跳过的页面
    for slide in pending_slides:
        show_preview_to_user(slide)
        user_feedback = wait_for_user_review()
        # ... 处理用户意见
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
