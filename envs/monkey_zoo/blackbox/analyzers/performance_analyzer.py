import logging
from datetime import timedelta

from envs.monkey_zoo.blackbox.analyzers.analyzer import Analyzer
from envs.monkey_zoo.blackbox.analyzers.analyzer_log import AnalyzerLog
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient

MAX_ALLOWED_SINGLE_PAGE_TIME = timedelta(seconds=1)
MAX_ALLOWED_TOTAL_TIME = timedelta(seconds=3)

logger = logging.getLogger(__name__)


class PerformanceAnalyzer(Analyzer):

    def __init__(self, island_client: MonkeyIslandClient, break_if_took_too_long=False):
        self.break_if_took_too_long = break_if_took_too_long
        self.island_client = island_client
        self.log = AnalyzerLog(self.__class__.__name__)

    def analyze_test_results(self) -> bool:
        self.log.clear()

        if not self.island_client.is_all_monkeys_dead():
            self.log.add_entry("Can't test report times since not all Monkeys have died.")
            return False

        total_time = timedelta()

        self.island_client.clear_caches()
        timings = self.island_client.time_all_report_pages()

        single_page_time_less_then_max = True

        for page, elapsed in timings.items():
            self.log.add_entry(f"page {page} took {str(elapsed)}")
            total_time += elapsed
            if elapsed > MAX_ALLOWED_SINGLE_PAGE_TIME:
                single_page_time_less_then_max = False

        total_time_less_then_max = total_time < MAX_ALLOWED_TOTAL_TIME

        self.log.add_entry(f"total time is {str(total_time)}")

        if self.break_if_took_too_long and (not (total_time_less_then_max and single_page_time_less_then_max)):
            logger.warning(
                "Calling breakpoint - pausing to enable investigation of island. Type 'c' to continue once you're done "
                "investigating. type 'p timings' and 'p total_time' to see performance information."
            )
            breakpoint()

        return total_time_less_then_max and single_page_time_less_then_max
