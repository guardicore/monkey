import logging
from datetime import timedelta

from envs.monkey_zoo.blackbox.analyzers.analyzer import Analyzer
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient

MAX_ALLOWED_SINGLE_PAGE_TIME = timedelta(seconds=2)
MAX_ALLOWED_TOTAL_TIME = timedelta(seconds=5)

logger = logging.getLogger(__name__)


class PerformanceAnalyzer(Analyzer):

    def __init__(self, island_client: MonkeyIslandClient, break_if_took_too_long=False):
        self.break_if_took_too_long = break_if_took_too_long
        self.island_client = island_client

    def analyze_test_results(self) -> bool:
        if not self.island_client.is_all_monkeys_dead():
            logger.info("Can't test report times since not all Monkeys have died.")
            return False

        total_time = timedelta()

        self.island_client.clear_caches()
        timings = self.island_client.time_all_report_pages()

        single_page_time_less_then_max = True

        for page, elapsed in timings.items():
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
