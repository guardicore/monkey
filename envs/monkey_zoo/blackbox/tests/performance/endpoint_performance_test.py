import logging

from envs.monkey_zoo.blackbox.analyzers.performance_analyzer import PerformanceAnalyzer
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient
from envs.monkey_zoo.blackbox.island_client.supported_request_method import SupportedRequestMethod
from envs.monkey_zoo.blackbox.tests.basic_test import BasicTest
from envs.monkey_zoo.blackbox.tests.performance.performance_test_config import PerformanceTestConfig

LOGGER = logging.getLogger(__name__)


class EndpointPerformanceTest(BasicTest):

    def __init__(self, name, test_config: PerformanceTestConfig, island_client: MonkeyIslandClient):
        self.name = name
        self.test_config = test_config
        self.island_client = island_client

    def run(self) -> bool:
        if not self.island_client.is_all_monkeys_dead():
            raise RuntimeError("Can't test report times since not all Monkeys have died.")

        # Collect timings for all pages
        self.island_client.clear_caches()
        endpoint_timings = {}
        for endpoint in self.test_config.endpoints_to_test:
            endpoint_timings[endpoint] = self.island_client.requests.get_request_time(endpoint,
                                                                                      SupportedRequestMethod.GET)
        analyzer = PerformanceAnalyzer(self.test_config, endpoint_timings)

        return analyzer.analyze_test_results()
