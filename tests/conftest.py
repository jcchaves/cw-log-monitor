import asyncio
from logging.config import dictConfig
import pytest

logger_format = "%(asctime)s:%(threadName)s:%(name)s:%(message)s"
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": logger_format,
                "datefmt": "%Y-%m-%dT%H:%M:%S %z",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "fileHandler": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": "log_monitor_test.log",
                "level": "DEBUG",
                "maxBytes": 1024000,
                "backupCount": 3,
            },
        },
        "loggers": {
            "root": {
                "handlers": ["console", "fileHandler"],
                "level": "DEBUG",
            },
            "helpers.cw_log_consumer": {
                "level": "DEBUG",
            },
            "helpers.cw_log_monitor": {
                "level": "DEBUG",
            },
            "helpers.cw_log_producer": {
                "level": "DEBUG",
            },
        },
    }
)


@pytest.fixture
def test_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.stop()
