"""Workspace manager for SCI-two-ppt.

Manages the working directory where all intermediate files, assets,
and outputs are stored during a PPT generation session.
"""

from pathlib import Path
from datetime import datetime
import shutil


class Workspace:
    def __init__(self, base_path: str = "./workspace"):
        self.path = Path(base_path).resolve()
        self.created_at: str | None = None

    def ensure_exists(self) -> Path:
        """Create workspace and all subdirectories if they don't exist."""
        dirs = [
            self.path,
            self.path / "agent_results",
            self.path / "preview",
            self.path / "assets",
            self.path / "assets" / "figures",
            self.path / "assets" / "images",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

        return self.path

    def save_artifact(self, name: str, content: str) -> Path:
        """Save a text artifact (markdown, yaml, etc.) to workspace."""
        self.ensure_exists()
        target = self.path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def list_artifacts(self) -> list[Path]:
        """List all files in workspace (excluding subdirectories)."""
        if not self.path.exists():
            return []
        return [p for p in self.path.rglob("*") if p.is_file()]

    def clean(self, keep_final: bool = True) -> None:
        """Clean intermediate files, optionally keeping final outputs."""
        if not self.path.exists():
            return

        intermediates = [
            self.path / "agent_results",
            self.path / "preview",
        ]
        for d in intermediates:
            if d.exists():
                shutil.rmtree(d)

    def get_summary(self) -> dict:
        """Get a summary of workspace contents."""
        if not self.path.exists():
            return {"exists": False, "path": str(self.path)}

        files = self.list_artifacts()
        return {
            "exists": True,
            "path": str(self.path),
            "file_count": len(files),
            "files": [str(f.relative_to(self.path)) for f in files[:50]],
            "created_at": self.created_at,
        }
