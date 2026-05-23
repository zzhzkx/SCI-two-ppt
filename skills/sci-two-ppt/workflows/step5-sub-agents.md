# Step 5: 子Agent生成SVG代码

## 概述

Step 5 是PPT制作的核心步骤，负责并行执行多个子Agent生成SVG代码。

## 角色

- **SVG Generator** (SVG生成器) - 生成SVG代码
- **Visual Designer** (视觉设计师) - 设计配色和布局
- **Material Collector** (素材搜集员) - 搜集图表素材

## 输入

- `workspace/goal.md` - PPT目标文档
- `workspace/papers/analysis.json` - 论文分析结果
- `workspace/papers/spec_lock.md` - 视觉规范

## 输出

- `workspace/preview/*.svg` - SVG文件

## SVG代码规范

### 画布尺寸
- **PPT 16:9**: 1280×720 像素
- **viewBox**: `0 0 1280 720`

### 颜色方案
使用 `spec_lock.md` 中定义的颜色：
```yaml
colors:
  primary: "#0D2137"
  secondary: "#1B6CA8"
  accent: "#FF6B35"
  background: "#FFFFFF"
  text: "#2D2D2D"
```

### 字体规范
- **标题**: Arial Bold 36pt
- **正文**: Arial 18pt
- **公式**: Cambria Math 20pt
- **图注**: Arial 14pt

### 坐标系统
- 使用像素坐标
- 原点在左上角
- X轴向右，Y轴向下

## 子Agent任务

### Agent 1: 封面SVG生成
```
输入: 论文标题、作者、单位、日期
输出: workspace/preview/slide_0.svg
SVG模板: 渐变背景 + 居中标题 + 副标题
```

### Agent 2: 内容页SVG生成
```
输入: 各章节标题和内容
输出: workspace/preview/slide_1.svg ~ slide_N.svg
SVG模板: 标题栏 + 左文右图布局
```

### Agent 3: 数据图表SVG生成
```
输入: 实验数据、误差分析结果
输出: workspace/preview/chart_*.svg
SVG模板: 柱状图、折线图、饼图
使用: SvgGenerator.generate_bar_chart_svg()
```

### Agent 4: 技术示意图SVG生成
```
输入: 系统架构、光路设计
输出: workspace/preview/diagram_*.svg
SVG模板: 流程图、架构图、示意图
```

### Agent 5: 学术内容SVG生成
```
输入: 公式、变量说明
输出: workspace/preview/formula_*.svg
SVG模板: 公式框 + 变量说明表
```

## SVG代码示例

### 封面页
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0D2137"/>
      <stop offset="100%" stop-color="#1B6CA8"/>
    </linearGradient>
  </defs>
  <rect width="1280" height="720" fill="url(#bgGrad)"/>
  <text x="640" y="300" text-anchor="middle"
        font-family="Arial" font-size="48" font-weight="bold" fill="#FFFFFF">
    论文标题
  </text>
  <text x="640" y="400" text-anchor="middle"
        font-family="Arial" font-size="28" fill="#6699CC">
    作者 | 单位
  </text>
</svg>
```

### 内容页
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <rect width="1280" height="720" fill="#FFFFFF"/>
  <rect x="0" y="0" width="1280" height="80" fill="#0D2137"/>
  <text x="80" y="52" font-family="Arial" font-size="36" font-weight="bold" fill="#FFFFFF">
    章节标题
  </text>
  <text x="80" y="200" font-family="Arial" font-size="18" fill="#2D2D2D">
    内容文本...
  </text>
</svg>
```

### 柱状图
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <rect width="1280" height="720" fill="#FFFFFF"/>
  <text x="640" y="50" text-anchor="middle" font-family="Arial" font-size="28" font-weight="bold" fill="#2D2D2D">
    图表标题
  </text>
  <line x1="150" y1="600" x2="1150" y2="600" stroke="#E0E0E0" stroke-width="2"/>
  <line x1="150" y1="200" x2="150" y2="600" stroke="#E0E0E0" stroke-width="2"/>
  <rect x="200" y="200" width="80" height="400" fill="#1B6CA8" rx="4"/>
  <text x="240" y="190" text-anchor="middle" font-family="Arial" font-size="14" fill="#2D2D2D">8.0</text>
  <text x="240" y="625" text-anchor="middle" font-family="Arial" font-size="12" fill="#2D2D2D">消光系数</text>
</svg>
```

## 质量检查

生成SVG后，调用 `check_svg_quality` 检查：
- ✅ viewBox格式正确
- ✅ 无禁止元素
- ✅ 字体安全
- ✅ 颜色符合规范
- ✅ 坐标在画布范围内

## 后续步骤

SVG生成完成后：
1. 调用 `check_svg_quality` 检查质量
2. 调用 `svg_to_pptx` 转换为PPTX
3. 生成预览，用户确认
4. 如需修改，返回本步骤重新生成
