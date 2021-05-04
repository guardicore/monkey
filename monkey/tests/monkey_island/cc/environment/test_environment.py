import os
import tempfile
from typing import Dict
from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytest

from common.utils.exceptions import (
    AlreadyRegisteredError,
    CredentialsNotRequiredError,
    InvalidRegistrationCredentialsError,
    RegistrationNotNeededError,
)
from monkey_island.cc.environment import Environment, EnvironmentConfig, UserCreds

WITH_CREDENTIALS = None
NO_CREDENTIALS = None
PARTIAL_CREDENTIALS = None
STANDARD_WITH_CREDENTIALS = None
STANDARD_ENV = None

EMPTY_CREDS = UserCreds("", "")


# This fixture is a dirty hack that can be removed once these tests are converted from
# unittest to pytest. Instead, the appropriate fixtures from conftest.py can be used.
@pytest.fixture(scope="module", autouse=True)
def configure_resources(environment_resources_dir):
    global WITH_CREDENTIALS
    global NO_CREDENTIALS
    global PARTIAL_CREDENTIALS
    global STANDARD_WITH_CREDENTIALS
    global STANDARD_ENV

    WITH_CREDENTIALS = os.path.join(
        environment_resources_dir, "server_config_with_credentials.json"
    )
    NO_CREDENTIALS = os.path.join(environment_resources_dir, "server_config_no_credentials.json")
    PARTIAL_CREDENTIALS = os.path.join(
        environment_resources_dir, "server_config_partial_credentials.json"
    )
    STANDARD_WITH_CREDENTIALS = os.path.join(
        environment_resources_dir, "server_config_standard_with_credentials.json"
    )
    STANDARD_ENV = os.path.join(environment_resources_dir, "server_config_standard_env.json")


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


def get_server_config_file_path_test_version():
    return os.path.join(os.getcwd(), "test_config.json")


class TestEnvironment(TestCase):
    class EnvironmentCredentialsNotRequired(Environment):
        def __init__(self):
            config = StubEnvironmentConfig("test", "test", EMPTY_CREDS)
            super().__init__(config)

        _credentials_required = False

        def get_auth_users(self):
            return []

    class EnvironmentCredentialsRequired(Environment):
        def __init__(self):
            config = StubEnvironmentConfig("test", "test", EMPTY_CREDS)
            super().__init__(config)

        _credentials_required = True

        def get_auth_users(self):
            return []

    class EnvironmentAlreadyRegistered(Environment):
        def __init__(self):
            config = StubEnvironmentConfig("test", "test", UserCreds("test_user", "test_secret"))
            super().__init__(config)

        _credentials_required = True

        def get_auth_users(self):
            return [1, "Test_username", "Test_secret"]

    @patch.object(target=EnvironmentConfig, attribute="save_to_file", new=MagicMock())
    def test_try_add_user(self):
        env = TestEnvironment.EnvironmentCredentialsRequired()
        credentials = UserCreds(username="test", password_hash="1231234")
        env.try_add_user(credentials)

        credentials = UserCreds(username="test", password_hash="")
        with self.assertRaises(InvalidRegistrationCredentialsError):
            env.try_add_user(credentials)

        env = TestEnvironment.EnvironmentCredentialsNotRequired()
        credentials = UserCreds(username="test", password_hash="1231234")
        with self.assertRaises(RegistrationNotNeededError):
            env.try_add_user(credentials)

    def test_try_needs_registration(self):
        env = TestEnvironment.EnvironmentAlreadyRegistered()
        with self.assertRaises(AlreadyRegisteredError):
            env._try_needs_registration()

        env = TestEnvironment.EnvironmentCredentialsNotRequired()
        with self.assertRaises(CredentialsNotRequiredError):
            env._try_needs_registration()

        env = TestEnvironment.EnvironmentCredentialsRequired()
        self.assertTrue(env._try_needs_registration())

    def test_needs_registration(self):
        env = TestEnvironment.EnvironmentCredentialsRequired()
        self._test_bool_env_method("needs_registration", env, WITH_CREDENTIALS, False)
        self._test_bool_env_method("needs_registration", env, NO_CREDENTIALS, True)
        self._test_bool_env_method("needs_registration", env, PARTIAL_CREDENTIALS, True)

        env = TestEnvironment.EnvironmentCredentialsNotRequired()
        self._test_bool_env_method("needs_registration", env, STANDARD_ENV, False)
        self._test_bool_env_method("needs_registration", env, STANDARD_WITH_CREDENTIALS, False)

    def test_is_registered(self):
        env = TestEnvironment.EnvironmentCredentialsRequired()
        self._test_bool_env_method("_is_registered", env, WITH_CREDENTIALS, True)
        self._test_bool_env_method("_is_registered", env, NO_CREDENTIALS, False)
        self._test_bool_env_method("_is_registered", env, PARTIAL_CREDENTIALS, False)

        env = TestEnvironment.EnvironmentCredentialsNotRequired()
        self._test_bool_env_method("_is_registered", env, STANDARD_ENV, False)
        self._test_bool_env_method("_is_registered", env, STANDARD_WITH_CREDENTIALS, False)

    def test_is_credentials_set_up(self):
        env = TestEnvironment.EnvironmentCredentialsRequired()
        self._test_bool_env_method("_is_credentials_set_up", env, NO_CREDENTIALS, False)
        self._test_bool_env_method("_is_credentials_set_up", env, WITH_CREDENTIALS, True)
        self._test_bool_env_method("_is_credentials_set_up", env, PARTIAL_CREDENTIALS, False)

        env = TestEnvironment.EnvironmentCredentialsNotRequired()
        self._test_bool_env_method("_is_credentials_set_up", env, STANDARD_ENV, False)

    def _test_bool_env_method(
        self, method_name: str, env: Environment, config: Dict, expected_result: bool
    ):
        env._config = EnvironmentConfig(config)
        method = getattr(env, method_name)
        if expected_result:
            self.assertTrue(method())
        else:
            self.assertFalse(method())
