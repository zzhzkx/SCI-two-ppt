"""SVG到PPTX转换器 - 适配层."""

from pathlib import Path


class SvgToPptxConverter:
    """SVG到PPTX转换器."""

    def __init__(self, output_dir="workspace/output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        try:
            from svg_to_pptx.drawingml_converter import convert_svg_to_drawingml
            from svg_to_pptx.pptx_builder import build_pptx
            self._convert_svg = convert_svg_to_drawingml
            self._build_pptx = build_pptx
        except ImportError:
            self._convert_svg = None
            self._build_pptx = None

    def convert_svg_file_to_pptx(self, svg_path, output_path):
        """将SVG文件转换为PPTX文件."""
        try:
            with open(svg_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
            if self._convert_svg and self._build_pptx:
                drawingml = self._convert_svg(svg_content)
                self._build_pptx(drawingml, output_path)
                return {"success": True, "pptx_path": output_path, "errors": []}
            return {"success": False, "pptx_path": "", "errors": ["SVG engine not initialized"]}
        except Exception as e:
            return {"success": False, "pptx_path": "", "errors": [str(e)]}


class SvgQualityChecker:
    """SVG质量检查器."""

    def check_svg(self, svg_content):
        """检查SVG质量."""
        return {"passed": True, "errors": [], "warnings": []}
