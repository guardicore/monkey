import unittest

import pytest

from envs.monkey_zoo.blackbox.monkey_island_client import MonkeyIslandClient
from envs.monkey_zoo.blackbox.analyzers.communication_analyzer import CommunicationAnalyzer
from envs.monkey_zoo.blackbox.island_config_parser import IslandConfigParser


def generic_blackbox_test_case(client, raw_config, analyzers):
    client.import_config(raw_config)
    # client.run_monkey_local()
    for analyzer in analyzers:
        assert analyzer.analyze_test_results()


@pytest.mark.usefixtures("island")
# noinspection PyUnresolvedReferences
class TestMonkeyBlackbox(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # GCPHandler().start_machines("elastic-4")
        print("Setting up all GCP machines...")

    @classmethod
    def tearDownClass(cls):
        # GCPHandler().stop_machines("elastic-4")
        print("Killing all GCP machines...")

    def test_server_online(self):
        client = MonkeyIslandClient(self.island)
        assert client.get_api_status() is not None

    def test_ssh_exec(self):
        conf_file_name = 'SSH.conf'
        client = MonkeyIslandClient(self.island)
        config_parser = IslandConfigParser(conf_file_name)
        analyzer = CommunicationAnalyzer(client, config_parser.get_ips_of_targets())
        generic_blackbox_test_case(client, config_parser.config_raw, [analyzer])


