class LogBase:
    def __init__(self, logs_client, log_group, log_stream):
        self.logs_client = logs_client
        self.log_group = log_group
        self.log_stream = log_stream
