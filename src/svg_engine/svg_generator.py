"""SVG生成器 - 生成符合PPT Master规范的SVG代码."""

from pathlib import Path
import json
import math


class SvgGenerator:
    """SVG代码生成器."""

    CANVAS_WIDTH = 1280
    CANVAS_HEIGHT = 720

    DEFAULT_COLORS = {
        "primary": "#0D2137",
        "secondary": "#1B6CA8",
        "accent": "#FF6B35",
        "background": "#FFFFFF",
        "text": "#2D2D2D",
        "light_gray": "#E0E0E0"
    }

    def __init__(self, colors: dict = None):
        self.colors = colors or self.DEFAULT_COLORS

    def generate_slide_svg(self, title="", content="", layout="content", notes="", subtitle="") -> str:
        """生成单页幻灯片的SVG代码."""
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

    def _generate_title_slide(self, title, subtitle=""):
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.CANVAS_WIDTH} {self.CANVAS_HEIGHT}">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{self.colors['primary']}"/>
      <stop offset="100%" stop-color="{self.colors['secondary']}"/>
    </linearGradient>
  </defs>
  <rect width="{self.CANVAS_WIDTH}" height="{self.CANVAS_HEIGHT}" fill="url(#bgGrad)"/>
  <text x="{self.CANVAS_WIDTH // 2}" y="300" text-anchor="middle" font-family="Arial" font-size="48" font-weight="bold" fill="{self.colors['background']}">{title}</text>
  <text x="{self.CANVAS_WIDTH // 2}" y="400" text-anchor="middle" font-family="Arial" font-size="28" fill="{self.colors['secondary']}">{subtitle}</text>
</svg>'''

    def _generate_content_slide(self, title, content):
        content_lines = content.split('\n')
        content_svg = ""
        y_pos = 200
        for line in content_lines[:8]:
            if line.strip():
                content_svg += f'  <text x="80" y="{y_pos}" font-family="Arial" font-size="18" fill="{self.colors["text"]}">{line.strip()}</text>\n'
                y_pos += 40

        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.CANVAS_WIDTH} {self.CANVAS_HEIGHT}">
  <rect width="{self.CANVAS_WIDTH}" height="{self.CANVAS_HEIGHT}" fill="{self.colors['background']}"/>
  <rect x="0" y="0" width="{self.CANVAS_WIDTH}" height="80" fill="{self.colors['primary']}"/>
  <text x="80" y="52" font-family="Arial" font-size="36" font-weight="bold" fill="{self.colors['background']}">{title}</text>
{content_svg}</svg>'''

    def generate_bar_chart_svg(self, title, values, labels=None, colors=None):
        """生成柱状图SVG."""
        if not labels:
            labels = [f"Item {i+1}" for i in range(len(values))]
        if not colors:
            colors = [self.colors['secondary'], self.colors['accent'], self.colors['primary'], "#4CAF50", "#9C27B0"]

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
            bars_svg += f'  <rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" fill="{color}" rx="4"/>\n'
            bars_svg += f'  <text x="{x + bar_width//2}" y="{y - 10}" text-anchor="middle" font-family="Arial" font-size="14" fill="{self.colors["text"]}">{val}</text>\n'
            bars_svg += f'  <text x="{x + bar_width//2}" y="{chart_bottom + 25}" text-anchor="middle" font-family="Arial" font-size="12" fill="{self.colors["text"]}">{label}</text>\n'

        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.CANVAS_WIDTH} {self.CANVAS_HEIGHT}">
  <rect width="{self.CANVAS_WIDTH}" height="{self.CANVAS_HEIGHT}" fill="{self.colors['background']}"/>
  <text x="{self.CANVAS_WIDTH // 2}" y="50" text-anchor="middle" font-family="Arial" font-size="28" font-weight="bold" fill="{self.colors['text']}">{title}</text>
  <line x1="150" y1="600" x2="1150" y2="600" stroke="{self.colors['light_gray']}" stroke-width="2"/>
  <line x1="150" y1="200" x2="150" y2="600" stroke="{self.colors['light_gray']}" stroke-width="2"/>
{bars_svg}</svg>'''

    def save_svg(self, svg_content, filename):
        output_dir = Path("workspace/preview")
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        return str(filepath)
