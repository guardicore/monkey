from datetime import timedelta
from typing import List


class PerformanceTestConfig:

    def __init__(self, max_allowed_single_page_time: timedelta, max_allowed_total_time: timedelta,
                 endpoints_to_test: List[str] = None, break_on_timeout=False):
        self.max_allowed_single_page_time = max_allowed_single_page_time
        self.max_allowed_total_time = max_allowed_total_time
        self.endpoints_to_test = endpoints_to_test
        self.break_on_timeout = break_on_timeout
