"""学术PPT规范库 - 配色/字体/排版规范."""

ACADEMIC_STYLES = {
    "optics": {
        "primary_color": "#003366",
        "secondary_color": "#6699CC",
        "accent_color": "#FF6600",
        "font_family": "Arial",
        "font_sizes": {"title": 36, "subtitle": 24, "body": 18, "caption": 14},
        "margins": {"top": 1.0, "bottom": 1.0, "left": 1.2, "right": 1.2},
        "description": "光学领域学术PPT - 深蓝色调，稳重专业"
    },
    "physics": {
        "primary_color": "#2C3E50",
        "secondary_color": "#3498DB",
        "accent_color": "#E74C3C",
        "font_family": "Calibri",
        "font_sizes": {"title": 36, "subtitle": 24, "body": 18, "caption": 14},
        "margins": {"top": 1.0, "bottom": 1.0, "left": 1.2, "right": 1.2},
        "description": "物理学领域 - 深灰蓝色调，严谨"
    },
    "chemistry": {
        "primary_color": "#1A5276",
        "secondary_color": "#2E86C1",
        "accent_color": "#27AE60",
        "font_family": "Arial",
        "font_sizes": {"title": 36, "subtitle": 24, "body": 18, "caption": 14},
        "margins": {"top": 1.0, "bottom": 1.0, "left": 1.2, "right": 1.2},
        "description": "化学领域 - 蓝绿色调，清新专业"
    },
    "computer_science": {
        "primary_color": "#2C3E50",
        "secondary_color": "#9B59B6",
        "accent_color": "#F39C12",
        "font_family": "Segoe UI",
        "font_sizes": {"title": 36, "subtitle": 24, "body": 18, "caption": 14},
        "margins": {"top": 1.0, "bottom": 1.0, "left": 1.2, "right": 1.2},
        "description": "计算机科学 - 紫色调，现代科技感"
    },
    "biology": {
        "primary_color": "#196F3D",
        "secondary_color": "#58D68D",
        "accent_color": "#E74C3C",
        "font_family": "Arial",
        "font_sizes": {"title": 36, "subtitle": 24, "body": 18, "caption": 14},
        "margins": {"top": 1.0, "bottom": 1.0, "left": 1.2, "right": 1.2},
        "description": "生物学领域 - 绿色调，生命科学"
    },
    "general": {
        "primary_color": "#1A5276",
        "secondary_color": "#2E86C1",
        "accent_color": "#E74C3C",
        "font_family": "Arial",
        "font_sizes": {"title": 36, "subtitle": 24, "body": 18, "caption": 14},
        "margins": {"top": 1.0, "bottom": 1.0, "left": 1.2, "right": 1.2},
        "description": "通用学术风格 - 蓝色调，专业通用"
    }
}


async def get_academic_style(domain: str = "general") -> dict:
    """获取学术PPT规范。

    Args:
        domain: 领域名称

    Returns:
        dict: 配色/字体/排版规范
    """
    if domain not in ACADEMIC_STYLES:
        domain = "general"
    style = ACADEMIC_STYLES[domain]
    return {
        "domain": domain,
        **style
    }


async def get_available_domains() -> list[str]:
    """获取所有可用的领域列表。"""
    return list(ACADEMIC_STYLES.keys())
