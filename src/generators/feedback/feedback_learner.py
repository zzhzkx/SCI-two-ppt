"""反馈学习系统 - 学习用户修改模式并应用到后续页面."""

from pathlib import Path
import json
from typing import Dict, List, Any


class FeedbackLearner:
    """学习用户修改模式的反馈系统."""

    def __init__(self, workspace_path: str = "workspace"):
        self.workspace_path = Path(workspace_path)
        self.feedback_dir = self.workspace_path / "feedback"
        self.feedback_dir.mkdir(parents=True, exist_ok=True)

        self.feedback_patterns = {
            "text_rewrites": [],
            "position_adjustments": [],
            "size_adjustments": [],
            "color_changes": []
        }

        self.modification_history = {}

    def learn_from_changes(self, changes: List[Dict], slide_index: int):
        """从变化中学习反馈模式.

        Args:
            changes: 变化列表
            slide_index: 幻灯片索引
        """
        for change in changes:
            if change["type"] == "text":
                self._learn_text_change(change, slide_index)
            elif change["type"] == "position":
                self._learn_position_change(change, slide_index)
            elif change["type"] == "size":
                self._learn_size_change(change, slide_index)
            elif change["type"] == "color":
                self._learn_color_change(change, slide_index)

        # 记录修改历史
        self.modification_history[f"slide_{slide_index}"] = {
            "changes": changes,
            "timestamp": self._get_timestamp()
        }

    def _learn_text_change(self, change: Dict, slide_index: int):
        """学习文本修改模式."""
        self.feedback_patterns["text_rewrites"].append({
            "original": change["original"],
            "modified": change["modified"],
            "slide": slide_index,
            "shape": change.get("shape", "")
        })

    def _learn_position_change(self, change: Dict, slide_index: int):
        """学习位置调整模式."""
        original = change["original"]
        modified = change["modified"]

        dx = modified["left"] - original["left"]
        dy = modified["top"] - original["top"]

        self.feedback_patterns["position_adjustments"].append({
            "shape": change.get("shape", ""),
            "dx": dx,
            "dy": dy,
            "slide": slide_index
        })

    def _learn_size_change(self, change: Dict, slide_index: int):
        """学习大小调整模式."""
        original = change["original"]
        modified = change["modified"]

        dw = modified["width"] - original["width"]
        dh = modified["height"] - original["height"]

        self.feedback_patterns["size_adjustments"].append({
            "shape": change.get("shape", ""),
            "dw": dw,
            "dh": dh,
            "slide": slide_index
        })

    def _learn_color_change(self, change: Dict, slide_index: int):
        """学习颜色变化模式."""
        self.feedback_patterns["color_changes"].append({
            "shape": change.get("shape", ""),
            "from_color": change["original"],
            "to_color": change["modified"],
            "slide": slide_index
        })

    def get_feedback_summary(self) -> Dict:
        """获取反馈摘要."""
        summary = {
            "total_feedback": sum(len(v) for v in self.feedback_patterns.values()),
            "patterns": {}
        }

        for pattern_type, patterns in self.feedback_patterns.items():
            if patterns:
                summary["patterns"][pattern_type] = {
                    "count": len(patterns),
                    "examples": patterns[:3]  # 最多3个示例
                }

        return summary

    def generate_feedback_report(self) -> str:
        """生成反馈报告."""
        summary = self.get_feedback_summary()

        report = f"""# User Feedback Report

## Summary
- Total feedback items: {summary['total_feedback']}

## Feedback Patterns

### Text Rewrites
{self._format_pattern_section(self.feedback_patterns['text_rewrites'])}

### Position Adjustments
{self._format_pattern_section(self.feedback_patterns['position_adjustments'])}

### Size Adjustments
{self._format_pattern_section(self.feedback_patterns['size_adjustments'])}

### Color Changes
{self._format_pattern_section(self.feedback_patterns['color_changes'])}

## Recommendations for Future Slides

Based on the feedback patterns:

1. **Text**: {self._get_text_recommendation()}
2. **Position**: {self._get_position_recommendation()}
3. **Size**: {self._get_size_recommendation()}
4. **Color**: {self._get_color_recommendation()}

## Modification History

{self._format_history()}
"""
        return report

    def _format_pattern_section(self, patterns: List[Dict]) -> str:
        """格式化模式部分."""
        if not patterns:
            return "- No patterns detected\n"

        lines = []
        for i, pattern in enumerate(patterns[:5], 1):  # 最多显示5个
            lines.append(f"- Pattern {i}: {json.dumps(pattern, indent=2)}")

        return "\n".join(lines) + "\n"

    def _get_text_recommendation(self) -> str:
        """获取文本修改建议."""
        if not self.feedback_patterns["text_rewrites"]:
            return "No text modifications detected"

        # 分析文本修改模式
        return "Consider adjusting text content based on user feedback"

    def _get_position_recommendation(self) -> str:
        """获取位置调整建议."""
        if not self.feedback_patterns["position_adjustments"]:
            return "No position adjustments detected"

        # 计算平均调整
        avg_dx = sum(p["dx"] for p in self.feedback_patterns["position_adjustments"]) / len(self.feedback_patterns["position_adjustments"])
        avg_dy = sum(p["dy"] for p in self.feedback_patterns["position_adjustments"]) / len(self.feedback_patterns["position_adjustments"])

        return f"Average position adjustment: dx={avg_dx:.2f}, dy={avg_dy:.2f}"

    def _get_size_recommendation(self) -> str:
        """获取大小调整建议."""
        if not self.feedback_patterns["size_adjustments"]:
            return "No size adjustments detected"

        return "Consider adjusting element sizes based on user feedback"

    def _get_color_recommendation(self) -> str:
        """获取颜色变化建议."""
        if not self.feedback_patterns["color_changes"]:
            return "No color changes detected"

        return "Consider adjusting colors based on user feedback"

    def _format_history(self) -> str:
        """格式化修改历史."""
        if not self.modification_history:
            return "No modifications recorded"

        lines = []
        for slide, data in self.modification_history.items():
            lines.append(f"- {slide}: {len(data['changes'])} changes at {data['timestamp']}")

        return "\n".join(lines)

    def _get_timestamp(self) -> str:
        """获取时间戳."""
        from datetime import datetime
        return datetime.now().isoformat()

    def apply_feedback_to_blueprint(self, blueprint: Dict) -> Dict:
        """将反馈应用到蓝图.

        Args:
            blueprint: 蓝图数据

        Returns:
            应用反馈后的蓝图
        """
        # 这里可以实现自动应用反馈的逻辑
        # 例如：调整后续页面的字体大小、位置等
        return blueprint

    def save_feedback(self):
        """保存反馈数据."""
        feedback_data = {
            "patterns": self.feedback_patterns,
            "history": self.modification_history,
            "timestamp": self._get_timestamp()
        }

        output_path = self.feedback_dir / "feedback_patterns.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(feedback_data, f, indent=2, ensure_ascii=False)

    def load_feedback(self):
        """加载反馈数据."""
        input_path = self.feedback_dir / "feedback_patterns.json"

        if input_path.exists():
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.feedback_patterns = data.get("patterns", self.feedback_patterns)
            self.modification_history = data.get("history", self.modification_history)
