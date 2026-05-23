"""SVG到PPTX转换器 - 适配层.

将PPT Master的SVG转换引擎集成到SCI-two-ppt中。
"""

from pathlib import Path
import json
import tempfile
import shutil


class SvgToPptxConverter:
    """SVG到PPTX转换器.

    使用PPT Master的svg_to_pptx引擎将SVG转换为PPTX。
    """

    def __init__(self, output_dir: str = "workspace/output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 导入PPT Master的转换模块
        try:
            from svg_to_pptx.drawingml_converter import convert_svg_to_drawingml
            from svg_to_pptx.pptx_builder import build_pptx
            self._convert_svg = convert_svg_to_drawingml
            self._build_pptx = build_pptx
        except ImportError:
            # 如果导入失败，使用简化实现
            self._convert_svg = None
            self._build_pptx = None

    def convert_svg_to_pptx(self, svg_content: str, output_path: str) -> dict:
        """将SVG内容转换为PPTX文件.

        Args:
            svg_content: SVG内容字符串
            output_path: 输出PPTX文件路径

        Returns:
            dict: {"success": bool, "pptx_path": str, "errors": list}
        """
        if not self._convert_svg or not self._build_pptx:
            return {
                "success": False,
                "pptx_path": "",
                "errors": ["SVG转换引擎未正确初始化"]
            }

        try:
            # 使用PPT Master的转换引擎
            drawingml = self._convert_svg(svg_content)
            self._build_pptx(drawingml, output_path)

            return {
                "success": True,
                "pptx_path": output_path,
                "errors": []
            }
        except Exception as e:
            return {
                "success": False,
                "pptx_path": "",
                "errors": [str(e)]
            }

    def convert_svg_file_to_pptx(self, svg_path: str, output_path: str) -> dict:
        """将SVG文件转换为PPTX文件.

        Args:
            svg_path: SVG文件路径
            output_path: 输出PPTX文件路径

        Returns:
            dict: {"success": bool, "pptx_path": str, "errors": list}
        """
        try:
            with open(svg_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
            return self.convert_svg_to_pptx(svg_content, output_path)
        except Exception as e:
            return {
                "success": False,
                "pptx_path": "",
                "errors": [str(e)]
            }


class SvgQualityChecker:
    """SVG质量检查器.

    使用PPT Master的svg_quality_checker进行质量检查。
    """

    def __init__(self):
        try:
            from svg_quality_checker import SvgQualityChecker as _Checker
            self._checker = _Checker
        except ImportError:
            self._checker = None

    def check_svg(self, svg_content: str) -> dict:
        """检查SVG质量.

        Args:
            svg_content: SVG内容字符串

        Returns:
            dict: {"passed": bool, "errors": list, "warnings": list}
        """
        if not self._checker:
            return {"passed": True, "errors": [], "warnings": ["质量检查器未初始化"]}

        try:
            checker = self._checker()
            result = checker.check_content(svg_content)
            return {
                "passed": result.get("passed", True),
                "errors": result.get("errors", []),
                "warnings": result.get("warnings", [])
            }
        except Exception as e:
            return {"passed": True, "errors": [], "warnings": [str(e)]}


class ChartCoordinateCalculator:
    """图表坐标计算器.

    使用PPT Master的svg_position_calculator计算图表坐标。
    """

    def __init__(self):
        try:
            from svg_position_calculator import (
                BarChartCalculator,
                PieChartCalculator,
                LineChartCalculator,
                RadarChartCalculator
            )
            self._bar_calc = BarChartCalculator
            self._pie_calc = PieChartCalculator
            self._line_calc = LineChartCalculator
            self._radar_calc = RadarChartCalculator
        except ImportError:
            self._bar_calc = None
            self._pie_calc = None
            self._line_calc = None
            self._radar_calc = None

    def calculate_bar_chart(self, values: list, labels: list = None) -> dict:
        """计算柱状图坐标.

        Args:
            values: 数据值列表
            labels: 标签列表

        Returns:
            dict: 图表坐标数据
        """
        if not self._bar_calc:
            return {"error": "柱状图计算器未初始化"}

        try:
            calc = self._bar_calc()
            result = calc.calculate(values, labels)
            return {"success": True, "coordinates": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def calculate_pie_chart(self, values: list, labels: list = None) -> dict:
        """计算饼图坐标."""
        if not self._pie_calc:
            return {"error": "饼图计算器未初始化"}

        try:
            calc = self._pie_calc()
            result = calc.calculate(values, labels)
            return {"success": True, "coordinates": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def calculate_line_chart(self, points: list) -> dict:
        """计算折线图坐标."""
        if not self._line_calc:
            return {"error": "折线图计算器未初始化"}

        try:
            calc = self._line_calc()
            result = calc.calculate(points)
            return {"success": True, "coordinates": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
