import logging
from datetime import datetime
from typing import Optional

LOGGER = logging.getLogger(__name__)


class IslandLogParser:
    def __init__(self, log_contents: str):
        self.log_contents = log_contents

    def filter_date(self, start: Optional[datetime] = None, end: Optional[datetime] = None) -> str:
        log_lines = self.log_contents.split("\n")
        if start:

            def filter_early(line):
                return self._get_date_from_line(line) > start

            log_lines = list(filter(filter_early, log_lines))
        if end:

            def filter_late(line):
                return self._get_date_from_line(line) < end

            log_lines = list(filter(filter_late, log_lines))
        return "\n".join(log_lines)

    @staticmethod
    def _get_date_from_line(line: str) -> datetime:
        logging.basicConfig()
        line_parts = line.split(" ")
        datetime_str = f"{line_parts[0]} {line_parts[1]}"

        # Logging uses only 3 digits for microseconds, when strptime expects 6
        # Reformat microseconds to have 6 digits
        datetime_str, microseconds = datetime_str.split(",")
        microseconds = str(int(microseconds) * 1000)
        datetime_str = f"{datetime_str}.{microseconds}"

        datetime_format = f"{logging.Formatter.default_time_format}.%f"
        return datetime.strptime(datetime_str, datetime_format)
