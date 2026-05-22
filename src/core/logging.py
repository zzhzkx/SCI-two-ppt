"""日志系统 for SCI-two-ppt MCP Server."""

import logging
import sys
from pathlib import Path
from src.core.config import load_config


def setup_logging(name: str = "sci-two-ppt") -> logging.Logger:
    """设置日志系统。

    Returns: 配置好的 Logger 实例
    """
    config = load_config()
    logger = logging.getLogger(name)

    if not logger.handlers:
        # 控制台输出
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(getattr(logging, config.log_level, logging.INFO))

        # 格式
        formatter = logging.Formatter(
            "[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 文件输出（可选）
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        file_handler = logging.FileHandler(
            log_dir / "sci-two-ppt.log",
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.setLevel(getattr(logging, config.log_level, logging.INFO))

    return logger


# 默认 logger 实例
logger = setup_logging()
