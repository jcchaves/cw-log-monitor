import asyncio
import boto3
from helpers.cw_log_monitor import LogMonitor
from helpers.cw_log_producer import LogProducer
import logging
import pytest

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
