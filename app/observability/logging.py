import logging
import sys
from ..config.authConfig import settings


def setup_logging():
    logger = logging.getLogger()

    formatter = logging.Formatter(settings.LOG_FORMAT)

    handlers = []

    # Console handler
    if settings.LOG_TO_CONSOLE:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        handlers.append(stream_handler)

    # File handler
    if settings.LOG_TO_FILE:
        file_handler = logging.FileHandler(settings.LOG_FILE)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    logger.handlers = handlers
    logger.setLevel(settings.LOG_LEVEL)