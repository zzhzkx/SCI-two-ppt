# src/styles/ 学术规范库指南

## 文件职责
- `academic_styles.py` - 学术PPT配色/字体/排版规范
- `slide_templates.py` - 页面模板库
- `citation_formats.py` - 引用格式规范

## 关键功能

### academic_styles.py
```python
async def get_academic_style(domain: str = "general") -> dict:
    """获取学术PPT规范。
    
    Input: domain - 领域(optics/physics/chemistry/computer_science/general)
    Output: {
        "primary_color": str,
        "secondary_color": str,
        "font_family": str,
        "font_sizes": {"title": int, "subtitle": int, "body": int},
        "margins": {"top": int, "bottom": int, "left": int, "right": int}
    }
    """
```

### slide_templates.py
```python
async def get_slide_template(slide_type: str) -> dict:
    """获取页面模板。
    
    Input: slide_type - title/content/chart/conclusion
    Output: {
        "layout": str,
        "elements": [...],
        "suggested_duration": int
    }
    """
```

### citation_formats.py
```python
async def get_citation_format(format_type: str = "IEEE") -> dict:
    """获取引用格式规范。
    
    Input: format_type - IEEE/APA/MLA
    Output: {
        "inline_format": str,
        "reference_format": str,
        "examples": [str]
    }
    """
```

## 数据文件
- `data/academic_styles.json` - 领域规范数据
