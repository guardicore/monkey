from unittest.mock import MagicMock

import dpath.util
import pytest

from common.config_value_paths import AWS_KEYS_PATH
from monkey_island.cc.database import mongo
from monkey_island.cc.server_utils.encryptor import get_encryptor, initialize_encryptor
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.zero_trust.scoutsuite.scoutsuite_auth_service import (
    is_aws_keys_setup,
)


class MockObject:
    pass


@pytest.mark.usefixtures("uses_database")
def test_is_aws_keys_setup(tmp_path):
    # Mock default configuration
    ConfigService.init_default_config()
    mongo.db = MockObject()
    mongo.db.config = MockObject()
    ConfigService.encrypt_config(ConfigService.default_config)
    mongo.db.config.find_one = MagicMock(return_value=ConfigService.default_config)
    assert not is_aws_keys_setup()

    # Make sure noone changed config path and broke this function
    initialize_encryptor(tmp_path)
    bogus_key_value = get_encryptor().enc("bogus_aws_key")
    dpath.util.set(
        ConfigService.default_config, AWS_KEYS_PATH + ["aws_secret_access_key"], bogus_key_value
    )
    dpath.util.set(
        ConfigService.default_config, AWS_KEYS_PATH + ["aws_access_key_id"], bogus_key_value
    )

    assert is_aws_keys_setup()
