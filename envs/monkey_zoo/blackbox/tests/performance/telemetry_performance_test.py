import json
from os import listdir
from os.path import isfile, join

from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient

TELEM_DIR_PATH = './tests/performance/test_telems'
TELEM_TEST_ENDPOINT = '/api/test/telemetry/performance'


class TelemetryPerformanceTest:

    def __init__(self, island_client: MonkeyIslandClient):
        self.island_client = island_client

    def test_telemetry_performance(self):
        all_telemetries = TelemetryPerformanceTest.get_all_telemetries()
        all_telemetries.sort(key=lambda telem: telem['time']['$date'])
        for telemetry in all_telemetries:
            self.send_telemetry(telemetry)

    @staticmethod
    def get_all_telemetries():
        telemetries = []
        file_paths = [join(TELEM_DIR_PATH, f) for f in listdir(TELEM_DIR_PATH) if isfile(join(TELEM_DIR_PATH, f))]
        for file_path in file_paths:
            with open(file_path, 'r') as telem_file:
                telem_contents = json.loads(telem_file.readline())
                telemetries.append(telem_contents)
        return telemetries

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
