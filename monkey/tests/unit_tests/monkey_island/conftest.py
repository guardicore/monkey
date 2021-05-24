import os

import pytest


@pytest.fixture(scope="module")
def server_configs_dir(data_for_tests_dir):
    return os.path.join(data_for_tests_dir, "server_configs")


@pytest.fixture(scope="module")
def server_config_init_only(server_configs_dir):
    return os.path.join(server_configs_dir, "server_config_init_only.json")


@pytest.fixture(scope="module")
def server_config_empty(server_configs_dir):
    return os.path.join(server_configs_dir, "server_config_empty.json")
