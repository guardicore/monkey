import unittest
from .gcp_machine_handlers import GCPHandler

import requests

from config import *


class TestMonkeyBlackbox(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        GCPHandler().start_machines("elastic-4")
        print("Setting up all GCP machines...")

    @classmethod
    def tearDownClass(cls):
        GCPHandler().stop_machines("elastic-4")
        print("Killing all GCP machines...")

    def generic_blackbox_test_case(self, config_file_path, analyzers):
        self.load_config_into_server(config_file_path)
        self.run_local_monkey_on_island()
        for analyzer in analyzers:
            assert analyzer.analyze_test_results()

    def load_config_into_server(self, config_file_path):
        print("uploading {} to {}".format(config_file_path, ISLAND_SERVER_ADDRESS))

    def run_local_monkey_on_island(self):
        print("Trying to run local monkey on {}".format(ISLAND_SERVER_ADDRESS))
        print(requests.get(ISLAND_SERVER_URL_FORMAT.format(resource="api"), verify=False).text)
