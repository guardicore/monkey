import re
from logging import Filter, LogRecord


class PyWSGILoggingFilter(Filter):
    """
    Remove the superfluous timestamp that gevent.pywsgi.WSGIServer inserts into its log messages

    The WSGIServer.format_request() hard-codes its own log format. This filter modifies the log
    message and removes the superfluous timestamp.

    See https://github.com/guardicore/monkey/issues/2059 for more information.
    """

    TIMESTAMP_REGEX = re.compile(r"- - \[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]")

    def filter(self, record: LogRecord) -> bool:
        """
        Remove the superfluous timestamp in gevent.pywsgi.WSGIServer log messages

        :param LogRecord: A log record to modify
        :return: True
        """

        record.msg = PyWSGILoggingFilter.TIMESTAMP_REGEX.sub("-", record.msg)
        return True
