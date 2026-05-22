"""学术规范库 - 配色/字体/模板/引用格式."""

from .academic_styles import get_academic_style, get_available_domains
from .slide_templates import get_slide_template, get_available_template_types
from .citation_formats import get_citation_format, get_available_formats

__all__ = [
    "get_academic_style",
    "get_available_domains",
    "get_slide_template",
    "get_available_template_types",
    "get_citation_format",
    "get_available_formats"
]
