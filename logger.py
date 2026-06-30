# Author: luedi
# Centralized logging configuration for RDDNS

import logging
import sys
from typing import Optional

_LOG_NAME = "rddns"


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """Configure the rddns logger.

    Idempotent — safe to call multiple times; only the first call sets up handlers.
    Later calls can change the log level via the already-configured logger.

    Args:
        level: One of DEBUG, INFO, WARNING, ERROR, CRITICAL (case-insensitive).
        log_file: Optional path to a log file. If set, logs are written to both
                  console and this file.

    Returns:
        The configured logger instance.
    """
    logger = logging.getLogger(_LOG_NAME)

    # Set level on every call so config changes take effect
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if not logger.handlers:
        fmt = logging.Formatter(
            "%(asctime)s [%(levelname)-7s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console handler
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(fmt)
        logger.addHandler(console)

        # Optional file handler
        if log_file:
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setFormatter(fmt)
            logger.addHandler(file_handler)

    return logger


def get_logger() -> logging.Logger:
    """Return the rddns logger without reconfiguring it.

    Use this in modules that are imported after setup_logging() has been called.
    """
    return logging.getLogger(_LOG_NAME)
