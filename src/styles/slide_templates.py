"""页面模板库 - 学术PPT预设布局."""

SLIDE_TEMPLATES = {
    "title": {
        "layout": "title_slide",
        "elements": ["title", "subtitle", "author", "institution", "date"],
        "suggested_duration": 30,
        "description": "封面页 - 论文标题、作者、单位、日期",
        "layout_spec": {
            "title": {"position": "center", "font_size": 40, "bold": True},
            "subtitle": {"position": "below_title", "font_size": 24},
            "author": {"position": "bottom", "font_size": 18},
            "institution": {"position": "below_author", "font_size": 16},
            "date": {"position": "bottom_right", "font_size": 14}
        }
    },
    "content": {
        "layout": "content_slide",
        "elements": ["title", "content_blocks", "figures"],
        "suggested_duration": 120,
        "description": "内容页 - 标题 + 正文/图表",
        "layout_spec": {
            "title": {"position": "top", "font_size": 32, "bold": True},
            "content_blocks": {"position": "main", "font_size": 18},
            "figures": {"position": "right_or_below", "max_width": 0.5}
        }
    },
    "two_column": {
        "layout": "two_column_slide",
        "elements": ["title", "left_content", "right_content"],
        "suggested_duration": 120,
        "description": "双栏页 - 标题 + 左右对比内容",
        "layout_spec": {
            "title": {"position": "top", "font_size": 32, "bold": True},
            "left_content": {"position": "left", "width": 0.45},
            "right_content": {"position": "right", "width": 0.45}
        }
    },
    "chart": {
        "layout": "chart_slide",
        "elements": ["title", "chart", "explanation"],
        "suggested_duration": 90,
        "description": "图表页 - 标题 + 图表 + 解释",
        "layout_spec": {
            "title": {"position": "top", "font_size": 32, "bold": True},
            "chart": {"position": "center", "max_height": 0.6},
            "explanation": {"position": "below_chart", "font_size": 16}
        }
    },
    "image": {
        "layout": "image_slide",
        "elements": ["title", "image", "caption"],
        "suggested_duration": 90,
        "description": "图片页 - 标题 + 大图 + 图注",
        "layout_spec": {
            "title": {"position": "top", "font_size": 32, "bold": True},
            "image": {"position": "center", "max_height": 0.65},
            "caption": {"position": "below_image", "font_size": 14, "italic": True}
        }
    },
    "comparison": {
        "layout": "comparison_slide",
        "elements": ["title", "before", "after", "arrow"],
        "suggested_duration": 120,
        "description": "对比页 - 前后/方法对比",
        "layout_spec": {
            "title": {"position": "top", "font_size": 32, "bold": True},
            "before": {"position": "left", "width": 0.4},
            "after": {"position": "right", "width": 0.4},
            "arrow": {"position": "center", "symbol": "->"}
        }
    },
    "bullet_points": {
        "layout": "bullet_slide",
        "elements": ["title", "bullets"],
        "suggested_duration": 90,
        "description": "要点页 - 标题 + 要点列表",
        "layout_spec": {
            "title": {"position": "top", "font_size": 32, "bold": True},
            "bullets": {"position": "main", "font_size": 20, "bullet_style": "dash"}
        }
    },
    "conclusion": {
        "layout": "conclusion_slide",
        "elements": ["title", "key_points", "future_work"],
        "suggested_duration": 60,
        "description": "总结页 - 核心结论 + 未来工作",
        "layout_spec": {
            "title": {"position": "top", "font_size": 36, "bold": True},
            "key_points": {"position": "main", "font_size": 20},
            "future_work": {"position": "bottom", "font_size": 16, "italic": True}
        }
    },
    "thank_you": {
        "layout": "thank_you_slide",
        "elements": ["title", "contact_info", "acknowledgments"],
        "suggested_duration": 30,
        "description": "致谢页 - 感谢 + 联系方式",
        "layout_spec": {
            "title": {"position": "center", "font_size": 44, "bold": True},
            "contact_info": {"position": "below_title", "font_size": 18},
            "acknowledgments": {"position": "bottom", "font_size": 14}
        }
    }
}


async def get_slide_template(slide_type: str) -> dict:
    """获取页面模板定义。

    Args:
        slide_type: 页面类型

    Returns:
        dict: 模板定义
    """
    template = SLIDE_TEMPLATES.get(slide_type, SLIDE_TEMPLATES["content"])
    return {
        "type": slide_type,
        **template
    }


async def get_available_template_types() -> list[str]:
    """获取所有可用的模板类型。"""
    return list(SLIDE_TEMPLATES.keys())
