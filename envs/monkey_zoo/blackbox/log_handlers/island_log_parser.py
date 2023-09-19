import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class IslandLogParser:
    def __init__(self, log_contents: str):
        self.log_contents = log_contents

    def filter_date(self, start: datetime) -> str:
        log_lines = self.log_contents.split("\n")
        test_start_index = 0
        for i in range(len(log_lines)):
            try:
                if self._get_date_from_line(log_lines[i]) < start:
                    continue
            except (ValueError, IndexError):
                continue
            test_start_index = i
            break

        return "\n".join(log_lines[test_start_index:])

    @staticmethod
    def _get_date_from_line(line: str) -> datetime:
        line_parts = line.split(" ")
        datetime_str = f"{line_parts[0]} {line_parts[1]}"

        # Logging uses only 3 digits for microseconds, when strptime expects 6
        # Reformat microseconds to have 6 digits
        datetime_str, microseconds = datetime_str.split(",")
        microseconds = str(int(microseconds) * 1000)
        datetime_str = f"{datetime_str}.{microseconds}"

        datetime_format = f"{logging.Formatter.default_time_format}.%f"
        return datetime.strptime(datetime_str, datetime_format)
