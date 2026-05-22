# src/core/ 核心模块指南

## 文件职责
- `config.py` - YAML配置加载器
- `workspace.py` - 工作空间管理器
- `logging.py` - 日志系统

## 关键类

### Config
```python
@dataclass
class Config:
    anthropic_api_key: str
    anthropic_model: str
    max_review_rounds: int
    default_workspace: str
    output_dir: str
    log_level: str
```

### Workspace
```python
class Workspace:
    def __init__(self, base_path: str = "./workspace")
    def ensure_exists(self) -> Path
    def save_artifact(self, name: str, content: str) -> Path
    def list_artifacts(self) -> list[Path]
    def clean(self, keep_final: bool = True)
    def get_summary(self) -> dict
```

## 使用方式
```python
from src.core.config import load_config
from src.core.workspace import Workspace

config = load_config()
ws = Workspace(config.default_workspace)
ws.ensure_exists()
ws.save_artifact("result.md", "# Result")
```

## 目录结构
workspace 会创建以下子目录:
- `agent_results/` - Agent 产出
- `preview/` - 预览文件
- `assets/figures/` - 图表资源
- `assets/images/` - 图片资源
