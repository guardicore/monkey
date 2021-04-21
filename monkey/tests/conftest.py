import os
import sys
from pathlib import Path

import pytest

MONKEY_BASE_PATH = str(Path(__file__).parent.parent)
sys.path.insert(0, MONKEY_BASE_PATH)


@pytest.fixture(scope="session")
def resources_dir(pytestconfig):
    return os.path.join(pytestconfig.rootdir, "monkey", "tests", "resources")


@pytest.fixture(scope="session")
def environment_resources_dir(resources_dir):
    return os.path.join(resources_dir, "environment")


@pytest.fixture(scope="session")
def with_credentials(environment_resources_dir):
    return os.path.join(environment_resources_dir, "server_config_with_credentials.json")


@pytest.fixture(scope="session")
def no_credentials(environment_resources_dir):
    return os.path.join(environment_resources_dir, "server_config_no_credentials.json")


@pytest.fixture(scope="session")
def partial_credentials(environment_resources_dir):
    return os.path.join(environment_resources_dir, "server_config_partial_credentials.json")


@pytest.fixture(scope="session")
def standard_with_credentials(environment_resources_dir):
    return os.path.join(environment_resources_dir, "server_config_standard_with_credentials.json")


@pytest.fixture(scope="session")
def with_data_dir(environment_resources_dir):
    return os.path.join(environment_resources_dir, "server_config_with_data_dir.json")


@pytest.fixture(scope="session")
def with_data_dir_home(environment_resources_dir):
    return os.path.join(environment_resources_dir, "server_config_with_data_dir_home.json")
