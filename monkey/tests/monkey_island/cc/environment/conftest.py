import os

import pytest


@pytest.fixture(scope="module")
def with_credentials(mocked_server_configs_dir):
    return os.path.join(mocked_server_configs_dir, "server_config_with_credentials.json")


@pytest.fixture(scope="module")
def no_credentials(mocked_server_configs_dir):
    return os.path.join(mocked_server_configs_dir, "server_config_no_credentials.json")


@pytest.fixture(scope="module")
def partial_credentials(mocked_server_configs_dir):
    return os.path.join(mocked_server_configs_dir, "server_config_partial_credentials.json")


@pytest.fixture(scope="module")
def standard_with_credentials(mocked_server_configs_dir):
    return os.path.join(mocked_server_configs_dir, "server_config_standard_with_credentials.json")
