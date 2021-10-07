import os
import tempfile
from typing import Dict
from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytest

from common.utils.exceptions import AlreadyRegisteredError, InvalidRegistrationCredentialsError
from monkey_island.cc.environment import Environment, EnvironmentConfig, UserCreds

WITH_CREDENTIALS = None
NO_CREDENTIALS = None
PARTIAL_CREDENTIALS = None

EMPTY_USER_CREDENTIALS = UserCreds("", "")
FULL_USER_CREDENTIALS = UserCreds(username="test", password_hash="1231234")


# This fixture is a dirty hack that can be removed once these tests are converted from
# unittest to pytest. Instead, the appropriate fixtures from conftest.py can be used.
@pytest.fixture(scope="module", autouse=True)
def configure_resources(server_configs_dir):
    global WITH_CREDENTIALS
    global NO_CREDENTIALS
    global PARTIAL_CREDENTIALS

    WITH_CREDENTIALS = os.path.join(server_configs_dir, "server_config_with_credentials.json")
    NO_CREDENTIALS = os.path.join(server_configs_dir, "server_config_no_credentials.json")
    PARTIAL_CREDENTIALS = os.path.join(server_configs_dir, "server_config_partial_credentials.json")


def get_tmp_file():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        return f.name


class StubEnvironmentConfig(EnvironmentConfig):
    def __init__(self, server_config, deployment, user_creds):
        self.server_config = server_config
        self.deployment = deployment
        self.user_creds = user_creds
        self.server_config_path = get_tmp_file()

    def __del__(self):
        os.remove(self.server_config_path)


class TestEnvironment(TestCase):
    class EnvironmentCredentialsRequired(Environment):
        def __init__(self):
            config = StubEnvironmentConfig("test", "test", EMPTY_USER_CREDENTIALS)
            super().__init__(config)

        def get_auth_users(self):
            return []

    class EnvironmentAlreadyRegistered(Environment):
        def __init__(self):
            config = StubEnvironmentConfig("test", "test", UserCreds("test_user", "test_secret"))
            super().__init__(config)

        def get_auth_users(self):
            return [1, "Test_username", "Test_secret"]

    @patch.object(target=EnvironmentConfig, attribute="save_to_file", new=MagicMock())
    def test_try_add_user(self):
        env = TestEnvironment.EnvironmentCredentialsRequired()
        credentials = FULL_USER_CREDENTIALS
        env.try_add_user(credentials)

        credentials = UserCreds(username="test", password_hash="")
        with self.assertRaises(InvalidRegistrationCredentialsError):
            env.try_add_user(credentials)

    def test_try_needs_registration(self):
        env = TestEnvironment.EnvironmentAlreadyRegistered()
        with self.assertRaises(AlreadyRegisteredError):
            env._try_needs_registration()

        env = TestEnvironment.EnvironmentCredentialsRequired()
        self.assertTrue(env._try_needs_registration())

    def test_needs_registration(self):
        env = TestEnvironment.EnvironmentCredentialsRequired()
        self._test_bool_env_method("needs_registration", env, WITH_CREDENTIALS, False)
        self._test_bool_env_method("needs_registration", env, NO_CREDENTIALS, True)
        self._test_bool_env_method("needs_registration", env, PARTIAL_CREDENTIALS, True)

    def test_is_registered(self):
        env = TestEnvironment.EnvironmentCredentialsRequired()
        self._test_bool_env_method("_is_registered", env, WITH_CREDENTIALS, True)
        self._test_bool_env_method("_is_registered", env, NO_CREDENTIALS, False)
        self._test_bool_env_method("_is_registered", env, PARTIAL_CREDENTIALS, False)

    def _test_bool_env_method(
        self, method_name: str, env: Environment, config: Dict, expected_result: bool
    ):
        env._config = EnvironmentConfig(config)
        method = getattr(env, method_name)
        if expected_result:
            self.assertTrue(method())
        else:
            self.assertFalse(method())
