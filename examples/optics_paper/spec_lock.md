# 视觉设计执行锁 - 微脉冲激光雷达系统设计

# 每页构建时必须读取此文件，确保一致性

# ============================================
# 颜色规范
# ============================================
colors:
  primary: "#003366"
  secondary: "#6699CC"
  accent: "#FF6600"
  background: "#FFFFFF"
  text_primary: "#333333"
  text_secondary: "#666666"
  text_light: "#FFFFFF"

# ============================================
# 字体规范
# ============================================
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

# ============================================
# 页面布局规范
# ============================================
layouts:
  title_slide:
    title_position: "center"
    subtitle_position: "below_title"
    background_type: "gradient"
    background_colors: ["#003366", "#6699CC"]
  
  content_slide:
    title_position: "top"
    content_position: "left"
    figure_position: "right"
    content_width: 0.55
    figure_width: 0.40
  
  chart_slide:
    title_position: "top"
    chart_position: "center"
    caption_position: "below_chart"
  
  conclusion_slide:
    title_position: "center"
    content_position: "center"
    background_type: "solid"
    background_color: "#003366"

# ============================================
# 图表规范
# ============================================
charts:
  style: "flat_modern"
  colors: ["#003366", "#6699CC", "#FF6600", "#4CAF50", "#9C27B0"]
  font_family: "Arial"
  font_size: 12
  grid: true
  grid_color: "#E0E0E0"
  legend_position: "top"

# ============================================
# 版本信息
# ============================================
version: "1.0"
created_at: "2026-05-22"
