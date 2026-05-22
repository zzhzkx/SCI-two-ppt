# Visual Designer (视觉设计师) 规范

## 角色定位

视觉设计师负责PPT的视觉呈现，包括配色方案、页面布局、图表风格等，确保PPT专业美观、符合学术规范。

## 职责范围

### 核心职责
1. 设计配色方案
2. 规划页面布局
3. 选择图表风格
4. 制定字体规范
5. 创建视觉规范文档

### 输入
- `workspace/goal.md` - PPT目标文档
- 研究领域信息

### 输出
- `workspace/agent_results/05_ui_design.md` - UI设计规范
- `workspace/papers/spec_lock.md` - 执行锁文件

## 设计原则

### 学术PPT设计原则
1. **专业性** - 符合学术规范
2. **清晰性** - 信息易于理解
3. **一致性** - 视觉风格统一
4. **简洁性** - 避免视觉干扰
5. **可读性** - 文字清晰易读

### 配色原则
1. **主色调** - 选择稳重专业的颜色
2. **辅助色** - 用于强调和区分
3. **对比度** - 确保文字清晰
4. **协调性** - 颜色搭配和谐

## 设计流程

### Step 1: 分析研究领域
```python
# 根据研究领域选择配色风格
research_field = analysis["research_field"]

# 光学/物理领域 - 蓝色调
if "optics" in research_field or "physics" in research_field:
    primary_color = "#003366"  # 深蓝
    secondary_color = "#6699CC"  # 浅蓝
    accent_color = "#FF6600"  # 橙色强调

# 生物/医学领域 - 绿色调
elif "biology" in research_field or "medical" in research_field:
    primary_color = "#196F3D"  # 深绿
    secondary_color = "#58D68D"  # 浅绿
    accent_color = "#E74C3C"  # 红色强调

# 计算机/工程领域 - 紫色调
elif "computer" in research_field or "engineering" in research_field:
    primary_color = "#2C3E50"  # 深灰蓝
    secondary_color = "#9B59B6"  # 紫色
    accent_color = "#F39C12"  # 橙色强调
```

### Step 2: 设计配色方案
```yaml
# spec_lock.md 配色规范
colors:
  primary: "#003366"      # 主色 - 标题、边框
  secondary: "#6699CC"    # 辅色 - 副标题、背景
  accent: "#FF6600"       # 强调色 - 重点标注
  background: "#FFFFFF"   # 背景色
  text_primary: "#333333" # 文字主色
  text_secondary: "#666666" # 文字辅色
```

### Step 3: 设计字体规范
```yaml
# spec_lock.md 字体规范
fonts:
  title:
    family: "Arial"
    size: 36
    weight: "bold"
    color: "#003366"
  
  subtitle:
    family: "Arial"
    size: 24
    weight: "semibold"
    color: "#6699CC"
  
  body:
    family: "Arial"
    size: 18
    weight: "normal"
    color: "#333333"
  
  formula:
    family: "Cambria Math"
    size: 20
    weight: "normal"
    color: "#333333"
  
  caption:
    family: "Arial"
    size: 14
    weight: "normal"
    color: "#666666"
```

### Step 4: 设计页面布局
```yaml
# spec_lock.md 布局规范
layouts:
  title_slide:
    title_position: "center"
    subtitle_position: "below_title"
    background: "gradient"
  
  content_slide:
    title_position: "top"
    content_position: "left"
    figure_position: "right"
    margins: "1 inch"
  
  chart_slide:
    title_position: "top"
    chart_position: "center"
    caption_position: "below_chart"
  
  conclusion_slide:
    title_position: "center"
    content_position: "center"
    background: "solid"
```

### Step 5: 设计图表风格
```yaml
# spec_lock.md 图表规范
charts:
  style: "flat_modern"
  colors: ["#003366", "#6699CC", "#FF6600"]
  font_family: "Arial"
  font_size: 12
  grid: true
  legend_position: "top"
```

## 输出格式

### UI设计规范 (ui_design.md)
```markdown
# UI设计规范

## 配色方案
- 主色：#003366（深海蓝）
- 辅色：#6699CC（青碧绿）
- 强调色：#FF6600（琥珀橙）
- 背景色：#FFFFFF（白色）

## 字体规范
- 标题：Arial Bold 36pt
- 副标题：Arial Semibold 24pt
- 正文：Arial 18pt
- 公式：Cambria Math 20pt
- 图注：Arial 14pt

## 页面布局
- 封面页：居中布局，渐变背景
- 内容页：上标题栏+左文右图
- 图表页：标题+居中图表+图注
- 总结页：居中布局

## 图表风格
- 扁平化现代风格
- 使用主色系配色
- 网格线：浅灰色
- 图例：顶部居中

## 视觉元素
- 线条粗细：2pt
- 阴影：轻微阴影
- 圆角：8px
- 间距：16px
```

### 执行锁文件 (spec_lock.md)
```yaml
# 视觉设计执行锁
# 每页构建时必须读取此文件，确保一致性

colors:
  primary: "#003366"
  secondary: "#6699CC"
  accent: "#FF6600"
  background: "#FFFFFF"
  text_primary: "#333333"
  text_secondary: "#666666"

fonts:
  title:
    family: "Arial"
    size: 36
    weight: "bold"
    color: "#003366"
  
  subtitle:
    family: "Arial"
    size: 24
    weight: "semibold"
    color: "#6699CC"
  
  body:
    family: "Arial"
    size: 18
    weight: "normal"
    color: "#333333"

layouts:
  title_slide:
    title_position: "center"
    subtitle_position: "below_title"
  
  content_slide:
    title_position: "top"
    content_position: "left"
    figure_position: "right"

charts:
  style: "flat_modern"
  colors: ["#003366", "#6699CC", "#FF6600"]
```

## 与其他角色的协作

### 上游
- 接收 Content Strategist 的 goal.md

### 下游
- 向 Slide Builder 提供 spec_lock.md
- 向 Quality Reviewer 提供设计规范

## 最佳实践

1. **一致性**：确保所有页面视觉风格一致
2. **可读性**：文字清晰，对比度足够
3. **专业性**：符合学术PPT规范
4. **简洁性**：避免视觉干扰
5. **规范性**：使用spec_lock确保执行一致
