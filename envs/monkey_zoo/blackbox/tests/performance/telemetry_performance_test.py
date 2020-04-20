

from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient
from envs.monkey_zoo.blackbox.tests.performance.utils.telem_parser import TelemParser


class TelemetryPerformanceTest:

    def __init__(self, island_client: MonkeyIslandClient):
        self.island_client = island_client

    def test_telemetry_performance(self):
        all_telemetries = TelemParser.get_all_telemetries()
        all_telemetries.sort(key=lambda telem: telem['time']['$date'])
        for telemetry in all_telemetries:
            self.send_telemetry(telemetry)

    def send_telemetry(self, telemetry):
        content = telemetry['content']
        url = telemetry['endpoint']
        method = telemetry['method']

        if method == 'POST':
            result = self.island_client.requests.post(url=url, data=content)
        elif method == 'GET':
            result = self.island_client.requests.get(url=url)
        elif method == 'PATCH':
            result = self.island_client.requests.patch_json(url=url, data=content)
        elif method == 'DELETE':
            result = self.island_client.requests.delete(url=url)
        else:
            raise Exception
        return result
