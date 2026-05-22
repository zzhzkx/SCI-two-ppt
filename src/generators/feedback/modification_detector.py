"""修改检测器 - 检测用户在PowerPoint中的手动修改."""

from pptx import Presentation
from pathlib import Path
import json


class ModificationDetector:
    """检测PPTX文件之间的变化."""

    def __init__(self):
        self.changes = []

    def detect_changes(self, original_path: str, modified_path: str) -> list:
        """检测两个PPTX文件之间的变化."""
        original = Presentation(original_path)
        modified = Presentation(modified_path)

        self.changes = []

        for slide_idx, (orig_slide, mod_slide) in enumerate(
            zip(original.slides, modified.slides)
        ):
            self._compare_slides(orig_slide, mod_slide, slide_idx)

        return self.changes

    def _compare_slides(self, orig_slide, mod_slide, slide_index: int):
        """比较两张幻灯片."""
        for orig_shape, mod_shape in zip(orig_slide.shapes, mod_slide.shapes):
            self._compare_shapes(orig_shape, mod_shape, slide_index)

    def _compare_shapes(self, orig_shape, mod_shape, slide_index: int):
        """比较两个形状."""
        shape_name = orig_shape.name

        # 检测文本变化
        if orig_shape.has_text_frame and mod_shape.has_text_frame:
            if orig_shape.text != mod_shape.text:
                self.changes.append({
                    "type": "text",
                    "slide": slide_index,
                    "shape": shape_name,
                    "original": orig_shape.text,
                    "modified": mod_shape.text
                })

        # 检测位置变化
        if (orig_shape.left != mod_shape.left or
            orig_shape.top != mod_shape.top):
            self.changes.append({
                "type": "position",
                "slide": slide_index,
                "shape": shape_name,
                "original": {"left": orig_shape.left, "top": orig_shape.top},
                "modified": {"left": mod_shape.left, "top": mod_shape.top}
            })

    def get_changes_summary(self) -> dict:
        """获取变化摘要."""
        return {"total_changes": len(self.changes)}

    def export_changes(self, output_path: str):
        """导出变化到JSON文件."""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.changes, f, indent=2, ensure_ascii=False)

    def has_significant_changes(self) -> bool:
        """检查是否有显著变化."""
        return len(self.changes) > 0
