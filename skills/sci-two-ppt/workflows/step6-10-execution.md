# Step 6-10: 审查确认、蓝图生成、逐页制作、最终打包

## Step 6: 审查确认

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
- ✅ 确认通过 → 进入Step 7
- ❌ 需要修改 → 返回Step 5重新执行相关Agent

---

## Step 7: PPT蓝图生成

### 7.1 综合所有信息
```python
goal = read_file("workspace/goal.md")
agent_results = read_directory("workspace/agent_results/")
ui_design = read_file("workspace/agent_results/05_ui_design.md")
chapter_structure = read_file("workspace/agent_results/06_chapter_structure.md")
```

### 7.2 生成蓝图
```yaml
slides:
  - index: 0
    type: title
    title: "论文标题"
    subtitle: "作者信息"
    notes: "开场白"
    duration_seconds: 30
    layout: "centered"
    
  - index: 1
    type: content
    title: "章节标题"
    content: "内容要点"
    figure: "figures/background.png"
    notes: "讲解备注"
    duration_seconds: 60
    layout: "left_text_right_image"
```

### 7.3 保存蓝图
保存到 `workspace/papers/blueprint.yaml`

---

## Step 8: 逐页制作PPT

### 8.1 判断制作方式

**SVG方式**（复杂页面）：
- 数据图表
- 技术示意图
- 复杂布局

**python-pptx方式**（简单页面）：
- 纯文字页面
- 简单布局

### 8.2 SVG制作流程

```python
for slide_def in blueprint["slides"]:
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
```

### 8.3 python-pptx制作流程

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

### 8.4 用户交互

**SVG方式**：
- 浏览器预览SVG
- 用户确认或修改
- 确认后转换为PPTX

**python-pptx方式**：
- HTML预览PPTX
- 用户在PowerPoint中修改
- 反馈修改意见

---

## Step 9: 最终打包

### 9.1 合并所有幻灯片
```python
final_pptx = merge_pptx_files(confirmed_slides)
```

### 9.2 添加全局元素
- 页码
- 页脚
- 动画效果（可选）

### 9.3 输出
- `workspace/output/final.pptx` - 最终PPT文件

---

## Step 10: 整理文件

### 10.1 清理中间文件
```python
# 保留重要文件
keep = [
    "workspace/output/final.pptx",
    "workspace/papers/",
    "workspace/agent_results/"
]

# 清理临时文件
clean = [
    "workspace/preview/*.svg",
    "workspace/preview/*.pptx",
    "workspace/preview/*.html"
]
```

### 10.2 生成制作报告
```markdown
# PPT制作报告

## 基本信息
- 论文标题：xxx
- 制作时间：xxx
- 总页数：xxx

## Agent产出统计
- 论文要点：完成
- 创新点：完成
- UI设计：完成
- 章节结构：完成
- 讲解备注：完成

## SVG生成统计
- 封面页：1页
- 内容页：N页
- 图表页：M页
- 技术示意图：K页

## 文件清单
- final.pptx - 最终PPT
- papers/ - 论文分析结果
- agent_results/ - Agent产出
```

### 10.3 最终产出
```
workspace/
├── output/
│   └── final.pptx              # 最终PPT
├── papers/
│   ├── analysis.json           # 论文分析
│   ├── goal.md                 # 目标文档
│   ├── requirements.md         # 需求文档
│   ├── blueprint.yaml          # PPT蓝图
│   └── spec_lock.md            # 视觉规范
├── agent_results/              # Agent产出
├── production_report.md        # 制作报告
└── README.md                   # 工作区说明
```

---

## 完整流程图

```
Step 6: 审查确认
    ↓ (通过)
Step 7: PPT蓝图生成
    ↓
Step 8: 逐页制作PPT
    ├─ SVG方式：生成SVG → 浏览器预览 → 确认 → 转换PPTX
    └─ python-pptx方式：直接生成PPTX → 预览 → 确认
    ↓ (所有页确认)
Step 9: 最终打包
    ↓
Step 10: 整理文件
```

## 错误处理

### Agent产出不足
```
用户反馈：缺少某些内容
    ↓
返回Step 5重新执行对应Agent
    ↓
补充内容后重新审查
```

### SVG质量检查失败
```
check_svg_quality() → 返回错误列表
    ↓
修正SVG代码
    ↓
重新检查
```

### 用户不满意PPT效果
```
用户反馈修改意见
    ↓
返回Step 8重新制作
    ↓
根据反馈调整
```
