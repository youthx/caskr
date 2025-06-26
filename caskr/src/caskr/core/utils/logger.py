import logging

from typing import Optional

from caskr.core.utils import env
from caskr.core.config import CaskrGlobalConf

def create_console_handler(level: int) -> logging.StreamHandler:
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    return handler

def setup_logger(name: Optional[str] = None, level: Optional[int] = None) -> logging.Logger:
    log_level = level or env.get_int("caskr_logger_level") or CaskrGlobalConf.DEFAULT_LOG_LEVEL
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Prevent adding multiple handlers if setup_logger called multiple times
    if not logger.hasHandlers():
        handler = create_console_handler(log_level)
        logger.addHandler(handler)

    # Optional: set some noisy third-party libs to WARNING by default
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    return logger

# Create a module-level logger for your app
logger = setup_logger(env.get("caskr_logger") or "caskr@root")

def set_log_level(level: int) -> None:
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)

def log(msg, *args, level=CaskrGlobalConf.DEFAULT_LOG_LEVEL, **kwargs):
    logger.log(level, msg, *args, **kwargs)