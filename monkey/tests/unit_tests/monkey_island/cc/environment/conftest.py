import os

import pytest


@pytest.fixture(scope="module")
def no_credentials(server_configs_dir):
    return os.path.join(server_configs_dir, "server_config_no_credentials.json")
