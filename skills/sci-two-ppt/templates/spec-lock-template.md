# 执行锁模板 (spec_lock.md)

## 使用说明

此模板用于生成机器可读的执行锁文件，确保每页PPT都符合视觉规范。Slide Builder在构建每页时必须读取此文件。

## 模板结构

```yaml
# 视觉设计执行锁
# 每页构建时必须读取此文件，确保一致性
# 由 Visual Designer 生成

# ============================================
# 颜色规范
# ============================================
colors:
  # 主色 - 标题、边框、主要元素
  primary: "#003366"
  
  # 辅色 - 副标题、背景、辅助元素
  secondary: "#6699CC"
  
  # 强调色 - 重点标注、数据高亮、关键信息
  accent: "#FF6600"
  
  # 背景色 - 幻灯片背景
  background: "#FFFFFF"
  
  # 文字颜色
  text_primary: "#333333"    # 主要文字
  text_secondary: "#666666"  # 次要文字
  text_light: "#FFFFFF"      # 浅色文字（深色背景上）

# ============================================
# 字体规范
# ============================================
fonts:
  # 主标题
  title:
    family: "Arial"
    size: 36
    weight: "bold"
    color: "#003366"
  
  # 副标题
  subtitle:
    family: "Arial"
    size: 24
    weight: "semibold"
    color: "#6699CC"
  
  # 正文
  body:
    family: "Arial"
    size: 18
    weight: "normal"
    color: "#333333"
  
  # 数学公式
  formula:
    family: "Cambria Math"
    size: 20
    weight: "normal"
    color: "#333333"
  
  # 图表说明
  caption:
    family: "Arial"
    size: 14
    weight: "normal"
    color: "#666666"
  
  # 强调文字
  emphasis:
    family: "Arial"
    size: 18
    weight: "bold"
    color: "#FF6600"

# ============================================
# 页面布局规范
# ============================================
layouts:
  # 封面页
  title_slide:
    title_position: "center"
    subtitle_position: "below_title"
    background_type: "gradient"
    background_colors: ["#003366", "#6699CC"]
    margin_top: 2.0  # 英寸
    margin_bottom: 1.0
  
  # 内容页
  content_slide:
    title_position: "top"
    title_height: 1.0
    content_position: "left"
    content_width: 0.55  # 55%宽度
    figure_position: "right"
    figure_width: 0.40   # 40%宽度
    margin_left: 1.0
    margin_right: 1.0
    margin_top: 0.5
    margin_bottom: 0.5
  
  # 图表页
  chart_slide:
    title_position: "top"
    title_height: 1.0
    chart_position: "center"
    chart_height: 5.0
    caption_position: "below_chart"
    caption_height: 0.5
  
  # 总结页
  conclusion_slide:
    title_position: "center"
    content_position: "center"
    background_type: "solid"
    background_color: "#003366"
    text_color: "#FFFFFF"
  
  # 致谢页
  thank_you_slide:
    title_position: "center"
    background_type: "gradient"
    background_colors: ["#003366", "#6699CC"]
    text_color: "#FFFFFF"

# ============================================
# 图表规范
# ============================================
charts:
  # 图表风格
  style: "flat_modern"
  
  # 图表配色（使用主色系）
  colors:
    - "#003366"
    - "#6699CC"
    - "#FF6600"
    - "#4CAF50"
    - "#9C27B0"
  
  # 字体设置
  font_family: "Arial"
  font_size: 12
  
  # 网格线
  grid: true
  grid_color: "#E0E0E0"
  grid_width: 0.5
  
  # 图例
  legend_position: "top"
  legend_font_size: 10
  
  # 坐标轴
  axis_color: "#333333"
  axis_width: 1.0
  
  # 数据标签
  data_labels: false
  data_label_font_size: 10

# ============================================
# 视觉元素规范
# ============================================
visual_elements:
  # 线条
  line_width: 2.0
  line_color: "#003366"
  
  # 阴影
  shadow: true
  shadow_color: "#000000"
  shadow_opacity: 0.2
  shadow_blur: 4
  
  # 圆角
  border_radius: 8
  
  # 间距
  spacing_small: 8
  spacing_medium: 16
  spacing_large: 24
  
  # 对齐
  alignment: "left"
  vertical_alignment: "top"

# ============================================
# 图标规范
# ============================================
icons:
  # 图标风格
  style: "outline"  # outline / filled / duotone
  
  # 图标颜色
  color: "#003366"
  
  # 图标大小
  size: 24
  
  # 图标库
  library: "tabler"  # tabler / phosphor / feather

# ============================================
# 动画规范
# ============================================
animations:
  # 页面切换
  page_transition: "fade"
  page_transition_duration: 0.5
  
  # 内容出现
  content_appear: "fade_in"
  content_appear_duration: 0.3
  content_appear_delay: 0.1
  
  # 图表动画
  chart_animation: "grow"
  chart_animation_duration: 0.5
  
  # 禁用的动画
  disabled:
    - "bounce"
    - "spin"
    - "flash"

# ============================================
# 特殊页面规范
# ============================================
special_pages:
  # 公式页
  formula_slide:
    formula_position: "center"
    formula_font_size: 24
    formula_color: "#003366"
    background: "#F5F5F5"
  
  # 数据展示页
  data_slide:
    data_highlight: "#FF6600"
    data_font_size: 36
    data_font_weight: "bold"
  
  # 对比页
  comparison_slide:
    left_color: "#003366"
    right_color: "#6699CC"
    divider_color: "#E0E0E0"

# ============================================
# 导出规范
# ============================================
export:
  # 文件格式
  format: "pptx"
  
  # 尺寸
  width: 13.333  # 英寸 (16:9)
  height: 7.5    # 英寸 (16:9)
  
  # 分辨率
  dpi: 300
  
  # 字体嵌入
  embed_fonts: true
  
  # 图片质量
  image_quality: 95

# ============================================
# 版本信息
# ============================================
version: "1.0"
created_by: "Visual Designer"
created_at: "2026-05-22"
updated_at: "2026-05-22"
```

## 使用方法

### Slide Builder 使用
```python
# 每页构建前读取spec_lock
spec_lock = read_yaml("workspace/papers/spec_lock.md")

# 应用颜色
apply_colors(slide, spec_lock["colors"])

# 应用字体
apply_fonts(slide, spec_lock["fonts"])

# 应用布局
apply_layout(slide, slide_type, spec_lock["layouts"])
```

### Visual Designer 生成
```python
# 根据研究领域生成spec_lock
spec_lock = generate_spec_lock(research_field, requirements)

# 保存到workspace
save_yaml("workspace/papers/spec_lock.md", spec_lock)
```

## 自定义说明

### 颜色自定义
根据研究领域调整配色：
- 光学/物理：蓝色调
- 生物/医学：绿色调
- 计算机/工程：紫色调

### 字体自定义
根据内容类型调整字体：
- 公式多：使用Cambria Math
- 中文多：使用微软雅黑
- 英文多：使用Arial

### 布局自定义
根据页面类型调整布局：
- 数据多：使用全宽图表
- 文字多：使用左文右图
- 图片多：使用居中大图
