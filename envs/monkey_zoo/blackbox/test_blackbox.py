import os
import unittest
from .gcp_machine_handlers import GCPHandler

import requests

from config import *

# SHA3-512 of '1234567890!@#$%^&*()_nothing_up_my_sleeve_1234567890!@#$%^&*()'
NO_AUTH_CREDS = '55e97c9dcfd22b8079189ddaeea9bce8125887e3237b800c6176c9afa80d2062' \
                '8d2c8d0b1538d2208c1444ac66535b764a3d902b35e751df3faec1e477ed3557'


def generic_blackbox_test_case(client, config_file_path, analyzers):
    load_config_into_server(client, config_file_path)
    run_local_monkey_on_island()
    for analyzer in analyzers:
        assert analyzer.analyze_test_results()


class MonkeyIslandClient(object):
    def __init__(self, server_address):
        self.addr = "https://{IP}/".format(IP=server_address)
        self.token = self.get_jwt_token_from_server()

    def get_jwt_token_from_server(self):
        resp = requests.post(self.addr + "api/auth", json={"username": NO_AUTH_CREDS, "password": NO_AUTH_CREDS}, verify=False)
        return resp.json()["access_token"]

    def get_api_status(self):
        return requests.get(self.addr + "api", headers={"Authorization": "JWT " + self.token}, verify=False)

    def import_config(self, config_contents):
        resp = requests.post(
            self.addr + "api/configuration/island",
            headers={"Authorization": "JWT " + self.token},
            data=config_contents,
            verify=False)
        print(resp.text)


class TestMonkeyBlackbox(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #GCPHandler().start_machines("elastic-4")
        print("Setting up all GCP machines...")

    @classmethod
    def tearDownClass(cls):
        #GCPHandler().stop_machines("elastic-4")
        print("Killing all GCP machines...")

    def test_server_online(self):
        client = MonkeyIslandClient(ISLAND_SERVER_ADDRESS)
        assert client.get_api_status() is not None

    def test_ssh_exec(self):
        client = MonkeyIslandClient(ISLAND_SERVER_ADDRESS)
        conf_file_name = "SSH.conf"
        generic_blackbox_test_case(client, get_conf_file_path(conf_file_name), [])


def run_local_monkey_on_island():
    print("Trying to run local monkey on {}".format(ISLAND_SERVER_ADDRESS))


def load_config_into_server(client, config_file_path):
    print("uploading {} to {}".format(config_file_path, ISLAND_SERVER_ADDRESS))
    with open(config_file_path, "r") as config_file:
        client.import_config(config_file.read())


def get_conf_file_path(conf_file_name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "island_configs", conf_file_name)
