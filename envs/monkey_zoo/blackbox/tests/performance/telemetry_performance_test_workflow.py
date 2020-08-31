from envs.monkey_zoo.blackbox.tests.basic_test import BasicTest
from envs.monkey_zoo.blackbox.tests.performance.endpoint_performance_test import \
    EndpointPerformanceTest
from envs.monkey_zoo.blackbox.tests.performance.performance_test_config import \
    PerformanceTestConfig
from envs.monkey_zoo.blackbox.tests.performance.telemetry_performance_test import \
    TelemetryPerformanceTest


class TelemetryPerformanceTestWorkflow(BasicTest):

    def __init__(self, name, island_client, performance_config: PerformanceTestConfig, quick_performance_test):
        self.name = name
        self.island_client = island_client
        self.performance_config = performance_config
        self.quick_performance_test = quick_performance_test

    def run(self):
        try:
            if not self.quick_performance_test:
                telem_sending_test = TelemetryPerformanceTest(island_client=self.island_client,
                                                              quick_performance_test=self.quick_performance_test)
                telem_sending_test.test_telemetry_performance()
            performance_test = EndpointPerformanceTest(self.name, self.performance_config, self.island_client)
            assert performance_test.run()
        finally:
            if not self.quick_performance_test:
                self.island_client.reset_env()
