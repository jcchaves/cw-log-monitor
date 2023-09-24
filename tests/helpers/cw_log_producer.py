from .cw_log_base import LogBase
import logging
import time

logger = logging.getLogger(__name__)


class LogProducer(LogBase):
    def __init__(self, logs_client, log_group, log_stream):
        super().__init__(logs_client, log_group, log_stream)

    def put_log_event(self, message):
        timestamp = int(round(time.time() * 1000))
        logger.info(f"Sending event '{message}' to log stream")
        response = self.logs_client.put_log_events(
            logGroupName=self.log_group,
            logStreamName=self.log_stream,
            logEvents=[
                {
                    "timestamp": timestamp,
                    "message": time.strftime("%Y-%m-%d %H:%M:%S") + f"\t{message}",
                }
            ],
        )
        logger.info(f"Log producer got this response: {response}")
