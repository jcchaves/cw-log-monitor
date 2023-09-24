import asyncio
import boto3
from helpers.cw_log_monitor import LogMonitor
from helpers.cw_log_producer import LogProducer
import logging
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

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_log_consumer(test_loop):
    session = boto3.Session(profile_name="clouddev")
    logs_client = session.client("logs")
    LOG_GROUP = "Main"
    LOG_STREAM = "Log Consumer"
    lmt = LogMonitor(
        loop=test_loop,
        logs_client=logs_client,
        log_group=LOG_GROUP,
        log_stream=LOG_STREAM,
    )
    lmt.start()

    log_producer = LogProducer(
        logs_client=logs_client,
        log_group=LOG_GROUP,
        log_stream=LOG_STREAM,
    )

    i = 0

    log_producer.put_log_event(f"Sending event #{i}")

    await asyncio.sleep(5)

    lmt.graceful_stop()

    while lmt.is_running():
        logger.info(f"Stopping Log Monitor thread...")
        await asyncio.sleep(1)


def main():
    pytest.main()


if __name__ == "__main__":
    main()
