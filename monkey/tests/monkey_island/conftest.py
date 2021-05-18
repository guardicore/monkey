import os

import pytest


@pytest.fixture(scope="module")
def mocked_server_configs_dir(mocked_data_dir):
    return os.path.join(mocked_data_dir, "server_configs")


@pytest.fixture(scope="module")
def test_server_config(mocked_server_configs_dir):
    return os.path.join(mocked_server_configs_dir, "test_server_config.json")
