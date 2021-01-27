from unittest.mock import MagicMock

import pytest
import dpath.util

from monkey_island.cc.database import mongo
from monkey_island.cc.server_utils import encryptor
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.config_schema.config_value_paths import AWS_KEYS_PATH
from monkey_island.cc.services.zero_trust.scoutsuite.scoutsuite_auth_service import is_aws_keys_setup
from monkey_island.cc.test_common.fixtures import FixtureEnum


class MockObject:
    pass

@pytest.mark.usefixtures(FixtureEnum.USES_DATABASE)
def test_is_aws_keys_setup():
    # Mock default configuration
    ConfigService.init_default_config()
    mongo.db = MockObject()
    mongo.db.config = MockObject()
    ConfigService.encrypt_config(ConfigService.default_config)
    mongo.db.config.find_one = MagicMock(return_value=ConfigService.default_config)
    assert not is_aws_keys_setup()

    # Make sure noone changed config path and broke this function
    bogus_key_value = encryptor.encryptor.enc('bogus_aws_key')
    dpath.util.set(ConfigService.default_config, AWS_KEYS_PATH+['aws_secret_access_key'], bogus_key_value)
    dpath.util.set(ConfigService.default_config, AWS_KEYS_PATH+['aws_access_key_id'], bogus_key_value)

    assert is_aws_keys_setup()
