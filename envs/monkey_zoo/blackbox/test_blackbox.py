import os
import unittest

import pytest

from envs.monkey_zoo.blackbox.monkey_island_client import MonkeyIslandClient


def generic_blackbox_test_case(client, config_file_path, analyzers):
    with open(config_file_path, "r") as config_file:
        client.import_config(config_file.read())
    # run_local_monkey_on_island()
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
        client = MonkeyIslandClient(self.island)
        conf_file_name = "SSH.conf"
        generic_blackbox_test_case(client, get_conf_file_path(conf_file_name), [])


def get_conf_file_path(conf_file_name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "island_configs", conf_file_name)
