import logging
import logging.config


class SensitiveDataFilter(logging.Filter):
    """Redacts sensitive fields from log records."""

    SENSITIVE_KEYS = {"password", "token", "access_token", "client_secret", "authorization"}

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.args, dict):
            record.args = {
                k: "***REDACTED***" if k.lower() in self.SENSITIVE_KEYS else v
                for k, v in record.args.items()
            }
        return True


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "[%(levelname)s] - %(asctime)s - %(name)s - %(message)s",
        },
    },
    "filters": {
        "sensitive_data_filter": {
            "()": SensitiveDataFilter,
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
            "filters": ["sensitive_data_filter"],
        },
        "file": {
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "filename": "my_log.log",
            "mode": "a",
            "maxBytes": 5_000_000,   # 5 MB per file
            "backupCount": 3,        # keep last 3 rotated files
        },
    },
    "loggers": {
        "app": {                          # covers all app.* modules
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "uvicorn": {                      # uvicorn access + error logs
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


def setup_logging() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
