import logging
from datetime import timedelta

from envs.monkey_zoo.blackbox.analyzers.analyzer import Analyzer
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient

MAX_ALLOWED_SINGLE_PAGE_TIME = timedelta(seconds=2)
MAX_ALLOWED_TOTAL_TIME = timedelta(seconds=5)

REPORT_URLS = [
    "api/report/security",
    "api/attack/report",
    "api/report/zero_trust/findings",
    "api/report/zero_trust/principles",
    "api/report/zero_trust/pillars"
]

logger = logging.getLogger(__name__)


class PerformanceAnalyzer(Analyzer):

    def __init__(self, island_client: MonkeyIslandClient, break_if_took_too_long=False):
        self.break_if_took_too_long = break_if_took_too_long
        self.island_client = island_client

    def analyze_test_results(self) -> bool:
        if not self.island_client.is_all_monkeys_dead():
            raise RuntimeError("Can't test report times since not all Monkeys have died.")

        # Collect timings for all pages
        self.island_client.clear_caches()
        report_resource_to_response_time = {}
        for url in REPORT_URLS:
            report_resource_to_response_time[url] = self.island_client.get_elapsed_for_get_request(url)

        # Calculate total time and check each page
        single_page_time_less_then_max = True
        total_time = timedelta()
        for page, elapsed in report_resource_to_response_time.items():
            logger.info(f"page {page} took {str(elapsed)}")
            total_time += elapsed
            if elapsed > MAX_ALLOWED_SINGLE_PAGE_TIME:
                single_page_time_less_then_max = False

        total_time_less_then_max = total_time < MAX_ALLOWED_TOTAL_TIME

        logger.info(f"total time is {str(total_time)}")

        performance_is_good_enough = total_time_less_then_max and single_page_time_less_then_max

        if self.break_if_took_too_long and not performance_is_good_enough:
            logger.warning(
                "Calling breakpoint - pausing to enable investigation of island. Type 'c' to continue once you're done "
                "investigating. Type 'p timings' and 'p total_time' to see performance information."
            )
            breakpoint()

        return performance_is_good_enough
