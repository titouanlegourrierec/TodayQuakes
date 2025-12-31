# Copyright (c) 2024 Titouan Le Gourrierec
"""Configure logging for the application."""

import logging
import time
from collections.abc import Callable
from typing import Any


logger = logging.getLogger(__name__)


def configure_logging() -> logging.Logger:
    """
    Configure logging for the application.

    Returns:
        logging.Logger: Configured logger instance.

    """
    logging.basicConfig(
        filename="log/log.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filemode="a"
    )
    logging.getLogger("matplotlib").setLevel(logging.ERROR)
    return logger


def log_execution_time(message: str | None = None) -> Callable:
    """
    Log the execution time of a function.

    Args:
        message (str | None): Optional message to include in the log.

    Returns:
        callable: Decorated function with execution time logging.

    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: tuple, **kwargs: dict) -> Any:  # noqa: ANN401
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            if message:
                msg = f"{message} ({func.__name__} executed in {execution_time:.2f} seconds)"  # ty: ignore[unresolved-attribute]
                logger.info(msg)
            else:
                msg = f"{func.__name__} executed in {execution_time:.2f} seconds"  # ty: ignore[unresolved-attribute]
                logger.info(msg)
            return result

        return wrapper

    return decorator
