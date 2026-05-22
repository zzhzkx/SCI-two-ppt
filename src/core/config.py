"""Configuration loader for SCI-two-ppt MCP Server."""

from dataclasses import dataclass, field
from pathlib import Path
import yaml


@dataclass
class Config:
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-20250514"
    max_review_rounds: int = 3
    default_workspace: str = "./workspace"
    output_dir: str = "./outputs"
    log_level: str = "INFO"


def load_config(config_path: str | None = None) -> Config:
    """Load configuration from YAML file.

    Search order:
    1. Explicit config_path argument
    2. config/settings.local.yaml (user overrides)
    3. config/settings.yaml (defaults)
    """
    search_paths = []
    if config_path:
        search_paths.append(Path(config_path))

    base = Path(__file__).parent.parent.parent
    search_paths.extend([
        base / "config" / "settings.local.yaml",
        base / "config" / "settings.yaml",
    ])

    for p in search_paths:
        if p.exists():
            with open(p, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            return _from_dict(data)

    return Config()


def _from_dict(data: dict) -> Config:
    cfg = Config()
    if "anthropic" in data:
        cfg.anthropic_api_key = data["anthropic"].get("api_key", "")
        cfg.anthropic_model = data["anthropic"].get("model", cfg.anthropic_model)
    if "pipeline" in data:
        cfg.max_review_rounds = data["pipeline"].get("max_review_rounds", cfg.max_review_rounds)
    if "output" in data:
        cfg.output_dir = data["output"].get("dir", cfg.output_dir)
    if "logging" in data:
        cfg.log_level = data["logging"].get("level", cfg.log_level)
    return cfg
