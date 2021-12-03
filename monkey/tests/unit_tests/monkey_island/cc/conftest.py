# Without these imports pytests can't use fixtures,
# because they are not found
import json
from typing import Dict

import pytest
from tests.unit_tests.monkey_island.cc.mongomock_fixtures import *  # noqa: F401,F403,E402
from tests.unit_tests.monkey_island.cc.server_utils.encryption.test_password_based_encryption import (  # noqa: E501
    FLAT_PLAINTEXT_MONKEY_CONFIG_FILENAME,
    MONKEY_CONFIGS_DIR_PATH,
    STANDARD_PLAINTEXT_MONKEY_CONFIG_FILENAME,
)

from monkey_island.cc.server_utils.encryption import unlock_datastore_encryptor


@pytest.fixture
def load_monkey_config(data_for_tests_dir) -> Dict:
    def inner(filename: str) -> Dict:
        config_path = (
            data_for_tests_dir / MONKEY_CONFIGS_DIR_PATH / FLAT_PLAINTEXT_MONKEY_CONFIG_FILENAME
        )
        return json.loads(open(config_path, "r").read())

    return inner


@pytest.fixture
def monkey_config(load_monkey_config):
    return load_monkey_config(STANDARD_PLAINTEXT_MONKEY_CONFIG_FILENAME)


@pytest.fixture
def flat_monkey_config(load_monkey_config):
    return load_monkey_config(FLAT_PLAINTEXT_MONKEY_CONFIG_FILENAME)


@pytest.fixture
def monkey_config_json(monkey_config):
    return json.dumps(monkey_config)


@pytest.fixture
def uses_encryptor(data_for_tests_dir):
    secret = "m0nk3y_u53r:3cr3t_p455w0rd"
    unlock_datastore_encryptor(data_for_tests_dir, secret)
