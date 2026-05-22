# src/parsers/ 解析模块指南

## 文件职责
- `paper_parser.py` - 论文PDF解析（基于PyMuPDF）
- `figure_extractor.py` - 图表提取
- `pptx_reader.py` - PPTX读取+差异对比

## 关键功能

### paper_parser.py
```python
async def parse_papers(papers: list[str]) -> dict:
    """解析论文PDF，提取结构化内容。
    
    Output: {
        "papers": [{
            "title": str,
            "abstract": str,
            "methods": str,
            "results": str,
            "figures": [{"path": str, "caption": str}],
            "key_findings": [str],
            "innovations": [str]
        }],
        "quality_report": str
    }
    """
```

### figure_extractor.py
```python
async def extract_figures(pdf_path: str) -> list[dict]:
    """提取PDF中的图表。
    
    Output: [{"path": str, "caption": str, "type": "figure|table"}]
    """
```

### pptx_reader.py
```python
async def read_pptx(pptx_path: str) -> dict:
    """读取PPTX文件状态。
    
    Output: {
        "slide_count": int,
        "slides": [{"index": int, "shapes": [...]}]
    }
    """

async def diff_pptx(original: str, modified: str) -> dict:
    """对比两版PPTX差异。
    
    Output: {
        "changes": [{"slide_index": int, "type": str, "detail": str}],
        "summary": str
    }
    """
```

## 依赖
- PyMuPDF (fitz) - PDF解析
- python-pptx - PPTX读写
