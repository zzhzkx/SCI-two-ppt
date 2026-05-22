"""反馈学习系统 - 学习用户修改模式并应用到后续页面."""

from pathlib import Path
import json
from typing import Dict, List


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

    def learn_from_changes(self, changes: List[Dict], slide_index: int):
        """从变化中学习反馈模式."""
        for change in changes:
            if change["type"] == "text":
                self.feedback_patterns["text_rewrites"].append({
                    "original": change["original"],
                    "modified": change["modified"],
                    "slide": slide_index
                })

    def get_feedback_summary(self) -> Dict:
        """获取反馈摘要."""
        return {
            "total_feedback": sum(len(v) for v in self.feedback_patterns.values()),
            "patterns": {k: len(v) for k, v in self.feedback_patterns.items()}
        }

    def generate_feedback_report(self) -> str:
        """生成反馈报告."""
        summary = self.get_feedback_summary()
        return f"""# Feedback Report

Total feedback: {summary['total_feedback']}

Patterns:
- Text rewrites: {summary['patterns']['text_rewrites']}
- Position adjustments: {summary['patterns']['position_adjustments']}
- Size adjustments: {summary['patterns']['size_adjustments']}
- Color changes: {summary['patterns']['color_changes']}
"""

    def save_feedback(self):
        """保存反馈数据."""
        output_path = self.feedback_dir / "feedback_patterns.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.feedback_patterns, f, indent=2, ensure_ascii=False)

    def load_feedback(self):
        """加载反馈数据."""
        input_path = self.feedback_dir / "feedback_patterns.json"
        if input_path.exists():
            with open(input_path, "r", encoding="utf-8") as f:
                self.feedback_patterns = json.load(f)
