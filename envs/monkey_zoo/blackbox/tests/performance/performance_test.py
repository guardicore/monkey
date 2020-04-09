import logging
from datetime import timedelta

from envs.monkey_zoo.blackbox.tests.basic_test import BasicTest
from envs.monkey_zoo.blackbox.tests.exploitation import ExploitationTest
from envs.monkey_zoo.blackbox.tests.performance.performance_test_config import PerformanceTestConfig
from envs.monkey_zoo.blackbox.analyzers.performance_analyzer import PerformanceAnalyzer


LOGGER = logging.getLogger(__name__)


class PerformanceTest(BasicTest):

    def __init__(self, name, test_config: PerformanceTestConfig, exploitation_test: ExploitationTest):
        self.name = name
        self.test_config = test_config
        self.exploitation_test = exploitation_test

    def run(self) -> bool:
        if not self.exploitation_test.island_client.is_all_monkeys_dead():
            raise RuntimeError("Can't test report times since not all Monkeys have died.")

        # Collect timings for all pages
        self.exploitation_test.island_client.clear_caches()
        endpoint_timings = {}
        for endpoint in self.test_config.endpoints_to_test:
            endpoint_timings[endpoint] = self.exploitation_test.island_client.get_elapsed_for_get_request(endpoint)

        analyzer = PerformanceAnalyzer(self.test_config, endpoint_timings)

        return analyzer.analyze_test_results()

    def get_elapsed_for_get_request(self, url):
        response = self.exploitation_test.island_client.requests.get(url)
        if response.ok:
            LOGGER.debug(f"Got ok for {url} content peek:\n{response.content[:120].strip()}")
            return response.elapsed
        else:
            LOGGER.error(f"Trying to get {url} but got unexpected {str(response)}")
            # instead of raising for status, mark failed responses as maxtime
            return timedelta.max()
