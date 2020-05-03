import logging
from datetime import timedelta
from typing import Dict

from envs.monkey_zoo.blackbox.analyzers.analyzer import Analyzer
from envs.monkey_zoo.blackbox.tests.performance.performance_test_config import PerformanceTestConfig
LOGGER = logging.getLogger(__name__)


class PerformanceAnalyzer(Analyzer):

    def __init__(self, performance_test_config: PerformanceTestConfig, endpoint_timings: Dict[str, timedelta]):
        self.performance_test_config = performance_test_config
        self.endpoint_timings = endpoint_timings

    def analyze_test_results(self):
        # Calculate total time and check each page
        single_page_time_less_then_max = True
        total_time = timedelta()
        for page, elapsed in self.endpoint_timings.items():
            LOGGER.info(f"page {page} took {str(elapsed)}")
            total_time += elapsed
            if elapsed > self.performance_test_config.max_allowed_single_page_time:
                single_page_time_less_then_max = False

        total_time_less_then_max = total_time < self.performance_test_config.max_allowed_total_time

        LOGGER.info(f"total time is {str(total_time)}")

        performance_is_good_enough = total_time_less_then_max and single_page_time_less_then_max

        if self.performance_test_config.break_on_timeout and not performance_is_good_enough:
            LOGGER.warning(
                "Calling breakpoint - pausing to enable investigation of island. Type 'c' to continue once you're done "
                "investigating. Type 'p timings' and 'p total_time' to see performance information."
            )
            breakpoint()

        return performance_is_good_enough
