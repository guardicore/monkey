import os

import pytest


@pytest.fixture(scope="module")
def with_credentials(server_configs_dir):
    return os.path.join(server_configs_dir, "server_config_with_credentials.json")


@pytest.fixture(scope="module")
def no_credentials(server_configs_dir):
    return os.path.join(server_configs_dir, "server_config_no_credentials.json")


@pytest.fixture(scope="module")
def partial_credentials(server_configs_dir):
    return os.path.join(server_configs_dir, "server_config_partial_credentials.json")
