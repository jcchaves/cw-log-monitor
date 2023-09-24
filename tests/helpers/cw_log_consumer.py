from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import logging
from .cw_log_base import LogBase

logger = logging.getLogger(__name__)


class LogConsumer(LogBase):
    def __init__(self, logs_client, log_group, log_stream):
        super().__init__(logs_client, log_group, log_stream)

    def get_log_events(self):
        end_time = datetime.now(tz=timezone.utc)
        start_time = end_time + relativedelta(minutes=-20)
        start_time = (int)(start_time.timestamp() * 1000)
        end_time = (int)(end_time.timestamp() * 1000)
        response = self.logs_client.get_log_events(
            logGroupName=self.log_group,
            logStreamName=self.log_stream,
            startTime=start_time,
            endTime=end_time,
        )
        return response
