from datetime import timedelta

from envs.monkey_zoo.blackbox.tests.basic_test import BasicTest
from envs.monkey_zoo.blackbox.tests.exploitation import ExploitationTest
from envs.monkey_zoo.blackbox.tests.performance.performance_test_config import PerformanceTestConfig
from envs.monkey_zoo.blackbox.tests.performance.performance_test import PerformanceTest

MAX_ALLOWED_SINGLE_PAGE_TIME = timedelta(seconds=2)
MAX_ALLOWED_TOTAL_TIME = timedelta(seconds=5)

REPORT_RESOURCES = [
    "api/report/security",
    "api/attack/report",
    "api/report/zero_trust/findings",
    "api/report/zero_trust/principles",
    "api/report/zero_trust/pillars"
]


class MapGenerationTest(BasicTest):

    def __init__(self, name, island_client, config_parser, analyzers,
                 timeout, log_handler, break_on_timeout=False):
        self.name = name
        self.island_client = island_client
        self.config_parser = config_parser
        self.exploitation_test = ExploitationTest(name, island_client, config_parser, analyzers, timeout, log_handler)
        self.break_on_timeout = break_on_timeout

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
            performance_config = PerformanceTestConfig(max_allowed_single_page_time=MAX_ALLOWED_SINGLE_PAGE_TIME,
                                                       max_allowed_total_time=MAX_ALLOWED_TOTAL_TIME,
                                                       endpoints_to_test=REPORT_RESOURCES,
                                                       break_on_timeout=self.break_on_timeout)
            performance_test = PerformanceTest("Report generation test", performance_config, self.exploitation_test)
            performance_test.run()
            self.exploitation_test.parse_logs()
            self.island_client.reset_env()
