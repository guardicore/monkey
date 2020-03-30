import logging
from datetime import timedelta

from envs.monkey_zoo.blackbox.tests.basic_test import BasicTest
from envs.monkey_zoo.blackbox.tests.exploitation import ExploitationTest

MAX_ALLOWED_SINGLE_PAGE_TIME = timedelta(seconds=2)
MAX_ALLOWED_TOTAL_TIME = timedelta(seconds=5)

REPORT_URLS = [
    "api/report/security",
    "api/attack/report",
    "api/report/zero_trust/findings",
    "api/report/zero_trust/principles",
    "api/report/zero_trust/pillars"
]

LOGGER = logging.getLogger(__name__)


class ReportGenerationTest(BasicTest):

    def __init__(self, name, island_client, config_parser, analyzers,
                 timeout, log_handler, break_if_took_too_long=False):
        self.name = name
        self.island_client = island_client
        self.config_parser = config_parser
        self.exploitation_test = ExploitationTest(name, island_client, config_parser, analyzers, timeout, log_handler)
        self.break_if_took_too_long = break_if_took_too_long

    def test_report_generation_performance(self) -> bool:
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
            LOGGER.info(f"page {page} took {str(elapsed)}")
            total_time += elapsed
            if elapsed > MAX_ALLOWED_SINGLE_PAGE_TIME:
                single_page_time_less_then_max = False

        total_time_less_then_max = total_time < MAX_ALLOWED_TOTAL_TIME

        LOGGER.info(f"total time is {str(total_time)}")

        performance_is_good_enough = total_time_less_then_max and single_page_time_less_then_max

        if self.break_if_took_too_long and not performance_is_good_enough:
            LOGGER.warning(
                "Calling breakpoint - pausing to enable investigation of island. Type 'c' to continue once you're done "
                "investigating. Type 'p timings' and 'p total_time' to see performance information."
            )
            breakpoint()

        return performance_is_good_enough

    def run(self):
        self.island_client.import_config(self.config_parser.config_raw)
        self.exploitation_test.print_test_starting_info()
        try:
            self.island_client.run_monkey_local()
            self.exploitation_test.test_until_timeout()
        finally:
            self.island_client.kill_all_monkeys()
            self.exploitation_test.wait_until_monkeys_die()
            self.exploitation_test.wait_for_monkey_process_to_finish()
            self.test_post_exec_analyzers()
            self.exploitation_test.parse_logs()
            self.island_client.reset_env()

    def test_post_exec_analyzers(self):
        post_exec_analyzers_results = [analyzer.analyze_test_results() for analyzer in self.post_exec_analyzers]
        assert all(post_exec_analyzers_results)
