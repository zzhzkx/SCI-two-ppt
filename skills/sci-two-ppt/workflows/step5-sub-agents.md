# Step 5: 子Agent生成SVG代码

## SVG规范

### 画布尺寸
- PPT 16:9: 1280×720 像素
- viewBox: `0 0 1280 720`

### 颜色方案
使用spec_lock中的配色

### 字体规范
- 标题: Arial Bold 36pt
- 正文: Arial 18pt
- 公式: Cambria Math 20pt

### 坐标系统
- 像素坐标
- 原点左上角

## 子Agent任务

1. 封面SVG - 渐变背景+标题
2. 内容页SVG - 标题栏+内容
3. 数据图表SVG - 柱状图/折线图
4. 技术示意图SVG - 架构图/流程图
5. 学术内容SVG - 公式/变量说明

详见完整文档。