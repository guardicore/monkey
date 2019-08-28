import os
import unittest
from .gcp_machine_handlers import GCPHandler

import requests

from config import *


def generic_blackbox_test_case(config_file_path, analyzers):
    load_config_into_server(config_file_path)
    run_local_monkey_on_island()
    for analyzer in analyzers:
        assert analyzer.analyze_test_results()


class TestMonkeyBlackbox(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        GCPHandler().start_machines("elastic-4")
        print("Setting up all GCP machines...")

    @classmethod
    def tearDownClass(cls):
        GCPHandler().stop_machines("elastic-4")
        print("Killing all GCP machines...")

    def test_ssh_exec(self):
        conf_file_name = "ssh.conf"
        generic_blackbox_test_case(get_conf_file_path(conf_file_name), [])


def run_local_monkey_on_island():
    print("Trying to run local monkey on {}".format(ISLAND_SERVER_ADDRESS))
    print(ISLAND_SERVER_URL + "api")


def load_config_into_server(config_file_path):
    print("uploading {} to {}".format(config_file_path, ISLAND_SERVER_ADDRESS))


def get_conf_file_path(conf_file_name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "island_configs", conf_file_name)
