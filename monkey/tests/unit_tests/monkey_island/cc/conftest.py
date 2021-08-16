# Without these imports pytests can't use fixtures,
# because they are not found
import json
import os

import pytest
from tests.unit_tests.monkey_island.cc.mongomock_fixtures import *  # noqa: F401,F403,E402
from tests.unit_tests.monkey_island.cc.services.utils.test_config_encryption import (
    MONKEY_CONFIGS_DIR_PATH,
    STANDARD_PLAINTEXT_MONKEY_CONFIG_FILENAME,
)


@pytest.fixture
def monkey_config(data_for_tests_dir):
    plaintext_monkey_config_standard_path = os.path.join(
        data_for_tests_dir, MONKEY_CONFIGS_DIR_PATH, STANDARD_PLAINTEXT_MONKEY_CONFIG_FILENAME
    )
    plaintext_config = json.loads(open(plaintext_monkey_config_standard_path, "r").read())
    return plaintext_config


@pytest.fixture
def monkey_config_json(monkey_config):
    return json.dumps(monkey_config)
