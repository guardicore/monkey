from envs.monkey_zoo.blackbox.tests.basic_test import BasicTest
from envs.monkey_zoo.blackbox.tests.exploitation import ExploitationTest
from envs.monkey_zoo.blackbox.tests.performance.endpoint_performance_test import \
    EndpointPerformanceTest
from envs.monkey_zoo.blackbox.tests.performance.performance_test_config import \
    PerformanceTestConfig


class PerformanceTestWorkflow(BasicTest):

    def __init__(self, name, exploitation_test: ExploitationTest, performance_config: PerformanceTestConfig):
        self.name = name
        self.exploitation_test = exploitation_test
        self.island_client = exploitation_test.island_client
        self.config_parser = exploitation_test.config_parser
        self.performance_config = performance_config

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
            if not self.island_client.is_all_monkeys_dead():
                raise RuntimeError("Can't test report times since not all Monkeys have died.")
        performance_test = EndpointPerformanceTest(self.name, self.performance_config, self.island_client)
        try:
            if not self.island_client.is_all_monkeys_dead():
                raise RuntimeError("Can't test report times since not all Monkeys have died.")
            assert performance_test.run()
        finally:
            self.exploitation_test.parse_logs()
            self.island_client.reset_env()
