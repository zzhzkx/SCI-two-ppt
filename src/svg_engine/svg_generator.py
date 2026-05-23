"""SVG生成器 - 生成符合PPT Master规范的SVG代码."""

from pathlib import Path
import json


class SvgGenerator:
    """SVG代码生成器.

    生成符合PPT Master规范的SVG代码，可以直接用于PPTX转换。
    """

    # PPT 16:9 画布尺寸
    CANVAS_WIDTH = 1280
    CANVAS_HEIGHT = 720

    # 默认颜色方案
    DEFAULT_COLORS = {
        "primary": "#0D2137",
        "secondary": "#1B6CA8",
        "accent": "#FF6B35",
        "background": "#FFFFFF",
        "text": "#2D2D2D",
        "light_gray": "#E0E0E0"
    }

    def __init__(self, colors: dict = None):
        """初始化SVG生成器.

        Args:
            colors: 自定义颜色方案
        """
        self.colors = colors or self.DEFAULT_COLORS

    def generate_slide_svg(
        self,
        title: str = "",
        content: str = "",
        layout: str = "content",
        notes: str = "",
        subtitle: str = ""
    ) -> str:
        """生成单页幻灯片的SVG代码.

        Args:
            title: 标题文本
            content: 内容文本
            layout: 布局类型 (title/content/chart/conclusion)
            notes: 备注文本
            subtitle: 副标题（用于标题页）

        Returns:
            str: SVG代码
        """
        if layout == "title":
            return self._generate_title_slide(title, subtitle=subtitle or content)
        elif layout == "content":
            return self._generate_content_slide(title, content)
        elif layout == "chart":
            return self._generate_chart_slide(title, content)
        elif layout == "conclusion":
            return self._generate_conclusion_slide(title, content)
        else:
            return self._generate_content_slide(title, content)

    def _generate_title_slide(self, title: str, subtitle: str = "") -> str:
        """生成标题页SVG."""
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.CANVAS_WIDTH} {self.CANVAS_HEIGHT}">
  <!-- 渐变背景 -->
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{self.colors['primary']}"/>
      <stop offset="100%" stop-color="{self.colors['secondary']}"/>
    </linearGradient>
  </defs>

  <!-- 背景 -->
  <rect width="{self.CANVAS_WIDTH}" height="{self.CANVAS_HEIGHT}" fill="url(#bgGrad)"/>

  <!-- 标题 -->
  <text x="{self.CANVAS_WIDTH // 2}" y="300" text-anchor="middle"
        font-family="Arial" font-size="48" font-weight="bold" fill="{self.colors['background']}">
    {title}
  </text>

  <!-- 副标题 -->
  <text x="{self.CANVAS_WIDTH // 2}" y="400" text-anchor="middle"
        font-family="Arial" font-size="28" fill="{self.colors['secondary']}">
    {subtitle}
  </text>
</svg>'''
        return svg

    def _generate_content_slide(self, title: str, content: str) -> str:
        """生成内容页SVG."""
        # 处理多行内容
        content_lines = content.split('\n')
        content_svg = ""
        y_pos = 200
        for line in content_lines[:8]:  # 最多8行
            if line.strip():
                content_svg += f'  <text x="80" y="{y_pos}" font-family="Arial" font-size="18" fill="{self.colors["text"]}">{line.strip()}</text>\n'
                y_pos += 40

        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.CANVAS_WIDTH} {self.CANVAS_HEIGHT}">
  <!-- 白色背景 -->
  <rect width="{self.CANVAS_WIDTH}" height="{self.CANVAS_HEIGHT}" fill="{self.colors['background']}"/>

  <!-- 标题栏 -->
  <rect x="0" y="0" width="{self.CANVAS_WIDTH}" height="80" fill="{self.colors['primary']}"/>
  <text x="80" y="52" font-family="Arial" font-size="36" font-weight="bold" fill="{self.colors['background']}">
    {title}
  </text>

  <!-- 内容区域 -->
{content_svg}
</svg>'''
        return svg

    def _generate_chart_slide(self, title: str, chart_description: str) -> str:
        """生成图表页SVG."""
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.CANVAS_WIDTH} {self.CANVAS_HEIGHT}">
  <!-- 白色背景 -->
  <rect width="{self.CANVAS_WIDTH}" height="{self.CANVAS_HEIGHT}" fill="{self.colors['background']}"/>

  <!-- 标题栏 -->
  <rect x="0" y="0" width="{self.CANVAS_WIDTH}" height="80" fill="{self.colors['primary']}"/>
  <text x="80" y="52" font-family="Arial" font-size="36" font-weight="bold" fill="{self.colors['background']}">
    {title}
  </text>

  <!-- 图表占位区域 -->
  <rect x="80" y="120" width="1120" height="520" fill="{self.colors['light_gray']}" rx="8"/>
  <text x="640" y="400" text-anchor="middle" font-family="Arial" font-size="24" fill="{self.colors['text']}">
    {chart_description}
  </text>
</svg>'''
        return svg

    def _generate_conclusion_slide(self, title: str, content: str) -> str:
        """生成结论页SVG."""
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.CANVAS_WIDTH} {self.CANVAS_HEIGHT}">
  <!-- 渐变背景 -->
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{self.colors['primary']}"/>
      <stop offset="100%" stop-color="{self.colors['secondary']}"/>
    </linearGradient>
  </defs>

  <rect width="{self.CANVAS_WIDTH}" height="{self.CANVAS_HEIGHT}" fill="url(#bgGrad)"/>

  <!-- 标题 -->
  <text x="{self.CANVAS_WIDTH // 2}" y="250" text-anchor="middle"
        font-family="Arial" font-size="44" font-weight="bold" fill="{self.colors['background']}">
    {title}
  </text>

  <!-- 内容 -->
  <text x="{self.CANVAS_WIDTH // 2}" y="350" text-anchor="middle"
        font-family="Arial" font-size="24" fill="{self.colors['secondary']}">
    {content}
  </text>
</svg>'''
        return svg

    def generate_bar_chart_svg(
        self,
        title: str,
        values: list,
        labels: list = None,
        colors: list = None
    ) -> str:
        """生成柱状图SVG.

        Args:
            title: 图表标题
            values: 数据值列表
            labels: 标签列表
            colors: 颜色列表

        Returns:
            str: SVG代码
        """
        if not labels:
            labels = [f"Item {i+1}" for i in range(len(values))]
        if not colors:
            colors = [self.colors['secondary'], self.colors['accent'],
                     self.colors['primary'], self.colors['light_gray']]

        # 计算柱状图参数
        max_val = max(values) if values else 1
        bar_width = 80
        gap = 40
        chart_left = 150
        chart_bottom = 600
        chart_height = 400

        bars_svg = ""
        for i, (val, label) in enumerate(zip(values, labels)):
            bar_height = (val / max_val) * chart_height
            x = chart_left + i * (bar_width + gap)
            y = chart_bottom - bar_height
            color = colors[i % len(colors)]

            bars_svg += f'''  <rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" fill="{color}" rx="4"/>
  <text x="{x + bar_width//2}" y="{y - 10}" text-anchor="middle" font-family="Arial" font-size="14" fill="{self.colors['text']}">{val}</text>
  <text x="{x + bar_width//2}" y="{chart_bottom + 25}" text-anchor="middle" font-family="Arial" font-size="12" fill="{self.colors['text']}">{label}</text>
'''

        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.CANVAS_WIDTH} {self.CANVAS_HEIGHT}">
  <!-- 白色背景 -->
  <rect width="{self.CANVAS_WIDTH}" height="{self.CANVAS_HEIGHT}" fill="{self.colors['background']}"/>

  <!-- 标题 -->
  <text x="{self.CANVAS_WIDTH // 2}" y="50" text-anchor="middle"
        font-family="Arial" font-size="28" font-weight="bold" fill="{self.colors['text']}">
    {title}
  </text>

  <!-- 图表区域 -->
  <line x1="150" y1="600" x2="1150" y2="600" stroke="{self.colors['light_gray']}" stroke-width="2"/>
  <line x1="150" y1="200" x2="150" y2="600" stroke="{self.colors['light_gray']}" stroke-width="2"/>

  <!-- 柱状图 -->
{bars_svg}
</svg>'''
        return svg

    def generate_pie_chart_svg(
        self,
        title: str,
        values: list,
        labels: list = None,
        colors: list = None
    ) -> str:
        """生成饼图SVG."""
        if not labels:
            labels = [f"Slice {i+1}" for i in range(len(values))]
        if not colors:
            colors = [self.colors['secondary'], self.colors['accent'],
                     self.colors['primary'], "#4CAF50", "#9C27B0"]

        total = sum(values) if values else 1
        center_x = self.CANVAS_WIDTH // 2
        center_y = self.CANVAS_HEIGHT // 2 + 50
        radius = 200

        slices_svg = ""
        start_angle = 0
        for i, (val, label) in enumerate(zip(values, labels)):
            angle = (val / total) * 360
            end_angle = start_angle + angle

            # 计算弧线端点
            import math
            start_rad = math.radians(start_angle)
            end_rad = math.radians(end_angle)

            x1 = center_x + radius * math.cos(start_rad)
            y1 = center_y + radius * math.sin(start_rad)
            x2 = center_x + radius * math.cos(end_rad)
            y2 = center_y + radius * math.sin(end_rad)

            large_arc = 1 if angle > 180 else 0
            color = colors[i % len(colors)]

            slices_svg += f'''  <path d="M {center_x} {center_y} L {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2} Z"
        fill="{color}" stroke="{self.colors['background']}" stroke-width="2"/>
  <text x="{center_x + (radius * 0.7 * math.cos(start_rad + (end_rad - start_rad) / 2))}"
        y="{center_y + (radius * 0.7 * math.sin(start_rad + (end_rad - start_rad) / 2))}"
        text-anchor="middle" font-family="Arial" font-size="14" fill="{self.colors['background']}">
    {label}
  </text>
'''
            start_angle = end_angle

        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.CANVAS_WIDTH} {self.CANVAS_HEIGHT}">
  <!-- 白色背景 -->
  <rect width="{self.CANVAS_WIDTH}" height="{self.CANVAS_HEIGHT}" fill="{self.colors['background']}"/>

  <!-- 标题 -->
  <text x="{self.CANVAS_WIDTH // 2}" y="50" text-anchor="middle"
        font-family="Arial" font-size="28" font-weight="bold" fill="{self.colors['text']}">
    {title}
  </text>

  <!-- 饼图 -->
{slices_svg}
</svg>'''
        return svg

    def save_svg(self, svg_content: str, filename: str) -> str:
        """保存SVG到文件.

        Args:
            svg_content: SVG内容
            filename: 文件名

        Returns:
            str: 文件路径
        """
        output_dir = Path("workspace/preview")
        output_dir.mkdir(parents=True, exist_ok=True)

        filepath = output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)

        return str(filepath)
