import json
import logging
from datetime import timedelta

from tqdm import tqdm

from envs.monkey_zoo.blackbox.analyzers.performance_analyzer import \
    PerformanceAnalyzer
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import \
    MonkeyIslandClient
from envs.monkey_zoo.blackbox.island_client.supported_request_method import \
    SupportedRequestMethod
from envs.monkey_zoo.blackbox.tests.performance.performance_test_config import \
    PerformanceTestConfig
from envs.monkey_zoo.blackbox.tests.performance.telem_sample_parsing.sample_file_parser import \
    SampleFileParser

LOGGER = logging.getLogger(__name__)

MAX_ALLOWED_SINGLE_TELEM_PARSE_TIME = timedelta(seconds=2)
MAX_ALLOWED_TOTAL_TIME = timedelta(seconds=60)


class TelemetryPerformanceTest:

    def __init__(self, island_client: MonkeyIslandClient, quick_performance_test: bool):
        self.island_client = island_client
        self.quick_performance_test = quick_performance_test

    def test_telemetry_performance(self):
        LOGGER.info("Starting telemetry performance test.")
        try:
            all_telemetries = SampleFileParser.get_all_telemetries()
        except FileNotFoundError:
            raise FileNotFoundError("Telemetries to send not found. "
                                    "Refer to readme to figure out how to generate telemetries and where to put them.")
        LOGGER.info("Telemetries imported successfully.")
        all_telemetries.sort(key=lambda telem: telem['time']['$date'])
        telemetry_parse_times = {}
        for telemetry in tqdm(all_telemetries, total=len(all_telemetries), ascii=True, desc="Telemetries sent"):
            telemetry_endpoint = TelemetryPerformanceTest.get_verbose_telemetry_endpoint(telemetry)
            telemetry_parse_times[telemetry_endpoint] = self.get_telemetry_time(telemetry)
        test_config = PerformanceTestConfig(MAX_ALLOWED_SINGLE_TELEM_PARSE_TIME, MAX_ALLOWED_TOTAL_TIME)
        PerformanceAnalyzer(test_config, telemetry_parse_times).analyze_test_results()
        if not self.quick_performance_test:
            self.island_client.reset_env()

    def get_telemetry_time(self, telemetry):
        content = telemetry['content']
        url = telemetry['endpoint']
        method = SupportedRequestMethod.__getattr__(telemetry['method'])

        return self.island_client.requests.get_request_time(url=url, method=method, data=content)

    @staticmethod
    def get_verbose_telemetry_endpoint(telemetry):
        telem_category = ""
        if "telem_category" in telemetry['content']:
            telem_category = "_" + json.loads(telemetry['content'])['telem_category'] + "_" + telemetry['_id']['$oid']
        return telemetry['endpoint'] + telem_category
