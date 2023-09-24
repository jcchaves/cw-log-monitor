import asyncio
from .cw_log_consumer import LogConsumer
import logging
from threading import Thread
import time

logger = logging.getLogger(__name__)


class LogMonitor(Thread):
    def __init__(
        self,
        loop,
        logs_client,
        log_group,
        log_stream,
    ):
        Thread.__init__(self)
        self._loop = loop
        self.keep_tailing = True
        self._running = False
        self.log_group = log_group
        self.log_stream = log_stream
        self.log_consumer = LogConsumer(
            logs_client=logs_client,
            log_group=log_group,
            log_stream=log_stream,
        )

    async def tail(self):
        try:
            log_events = self.log_consumer.get_log_events()
            for event in log_events["events"]:
                logger.info(
                    f"Log group: {self.log_group} - Log Stream: {self.log_stream} - Log event: {event['message']}"
                )
        except Exception as e:
            logger.error(f"{e}")
            raise

    def graceful_stop(self):
        self.keep_tailing = False

    def is_running(self):
        return self._running

    def run(self) -> None:
        self._running = True
        asyncio.set_event_loop(self._loop)
        logger.info(f"Tailing log group/log stream {self.log_group}/{self.log_stream}")
        while self.keep_tailing:
            asyncio.run(self.tail())
            asyncio.run(asyncio.sleep(1))
        self._running = False
