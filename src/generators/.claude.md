# src/generators/ 生成模块指南

## 文件职责
- `slide_builder.py` - 单页幻灯片生成
- `preview_renderer.py` - 预览图渲染
- `pptx_packager.py` - 最终PPTX打包

## 关键功能

### slide_builder.py
```python
async def build_slide(
    blueprint_yaml: str,
    slide_index: int,
    modifications: str = ""
) -> dict:
    """根据蓝图生成单页幻灯片。
    
    Output: {
        "pptx_path": str,
        "preview_image": str,
        "slide_index": int
    }
    """
```

### preview_renderer.py
```python
async def render_preview(pptx_path: str, slide_index: int) -> str:
    """渲染幻灯片为图片。
    
    Output: 预览图片路径
    """
```

### pptx_packager.py
```python
async def generate_pptx(
    blueprint: str,
    slide_dir: str,
    output_path: str
) -> dict:
    """最终打包生成PPTX。
    
    Output: {
        "pptx_path": str,
        "report_md": str,
        "slide_count": int
    }
    """
```

## 依赖
- python-pptx - PPT生成
- Pillow - 图片处理
- src/styles/ - 学术规范
