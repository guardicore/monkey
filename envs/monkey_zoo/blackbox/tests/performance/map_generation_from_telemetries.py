from datetime import timedelta

from envs.monkey_zoo.blackbox.tests.performance.performance_test import \
    PerformanceTest
from envs.monkey_zoo.blackbox.tests.performance.performance_test_config import \
    PerformanceTestConfig
from envs.monkey_zoo.blackbox.tests.performance.telemetry_performance_test_workflow import \
    TelemetryPerformanceTestWorkflow

MAX_ALLOWED_SINGLE_PAGE_TIME = timedelta(seconds=2)
MAX_ALLOWED_TOTAL_TIME = timedelta(seconds=5)

MAP_RESOURCES = [
    "api/netmap",
]


class MapGenerationFromTelemetryTest(PerformanceTest):

    TEST_NAME = "Map generation from fake telemetries test"

    def __init__(self, island_client, quick_performance_test: bool, break_on_timeout=False):
        self.island_client = island_client
        performance_config = PerformanceTestConfig(max_allowed_single_page_time=MAX_ALLOWED_SINGLE_PAGE_TIME,
                                                   max_allowed_total_time=MAX_ALLOWED_TOTAL_TIME,
                                                   endpoints_to_test=MAP_RESOURCES,
                                                   break_on_timeout=break_on_timeout)
        self.performance_test_workflow = TelemetryPerformanceTestWorkflow(MapGenerationFromTelemetryTest.TEST_NAME,
                                                                          self.island_client,
                                                                          performance_config,
                                                                          quick_performance_test)

    def run(self):
        self.performance_test_workflow.run()
