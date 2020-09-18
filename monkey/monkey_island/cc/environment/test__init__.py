import json
import os
from typing import Dict
from unittest import TestCase
from unittest.mock import MagicMock, patch

import monkey_island.cc.testing.environment.server_config_mocks as config_mocks
from common.utils.exceptions import (AlreadyRegisteredError,
                                     CredentialsNotRequiredError,
                                     InvalidRegistrationCredentialsError,
                                     RegistrationNotNeededError)
from monkey_island.cc.environment import (Environment, EnvironmentConfig,
                                          UserCreds)


def get_server_config_file_path_test_version():
    return os.path.join(os.getcwd(), 'test_config.json')


class TestEnvironment(TestCase):

    class EnvironmentCredentialsNotRequired(Environment):
        def __init__(self):
            config = EnvironmentConfig('test', 'test', UserCreds())
            super().__init__(config)

        _credentials_required = False

        def get_auth_users(self):
            return []

    class EnvironmentCredentialsRequired(Environment):
        def __init__(self):
            config = EnvironmentConfig('test', 'test', UserCreds())
            super().__init__(config)

        _credentials_required = True

        def get_auth_users(self):
            return []

    class EnvironmentAlreadyRegistered(Environment):
        def __init__(self):
            config = EnvironmentConfig('test', 'test', UserCreds('test_user', 'test_secret'))
            super().__init__(config)

        _credentials_required = True

        def get_auth_users(self):
            return [1, "Test_username", "Test_secret"]

    @patch.object(target=EnvironmentConfig, attribute="save_to_file", new=MagicMock())
    def test_try_add_user(self):
        env = TestEnvironment.EnvironmentCredentialsRequired()
        credentials = UserCreds(username="test", password_hash="1231234")
        env.try_add_user(credentials)

        credentials = UserCreds(username="test")
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
        self._test_bool_env_method("needs_registration", env, config_mocks.CONFIG_WITH_CREDENTIALS, False)
        self._test_bool_env_method("needs_registration", env, config_mocks.CONFIG_NO_CREDENTIALS, True)
        self._test_bool_env_method("needs_registration", env, config_mocks.CONFIG_PARTIAL_CREDENTIALS, True)

        env = TestEnvironment.EnvironmentCredentialsNotRequired()
        self._test_bool_env_method("needs_registration", env, config_mocks.CONFIG_STANDARD_ENV, False)
        self._test_bool_env_method("needs_registration", env, config_mocks.CONFIG_STANDARD_WITH_CREDENTIALS, False)

    def test_is_registered(self):
        env = TestEnvironment.EnvironmentCredentialsRequired()
        self._test_bool_env_method("_is_registered", env, config_mocks.CONFIG_WITH_CREDENTIALS, True)
        self._test_bool_env_method("_is_registered", env, config_mocks.CONFIG_NO_CREDENTIALS, False)
        self._test_bool_env_method("_is_registered", env, config_mocks.CONFIG_PARTIAL_CREDENTIALS, False)

        env = TestEnvironment.EnvironmentCredentialsNotRequired()
        self._test_bool_env_method("_is_registered", env, config_mocks.CONFIG_STANDARD_ENV, False)
        self._test_bool_env_method("_is_registered", env, config_mocks.CONFIG_STANDARD_WITH_CREDENTIALS, False)

    def test_is_credentials_set_up(self):
        env = TestEnvironment.EnvironmentCredentialsRequired()
        self._test_bool_env_method("_is_credentials_set_up", env, config_mocks.CONFIG_NO_CREDENTIALS, False)
        self._test_bool_env_method("_is_credentials_set_up", env, config_mocks.CONFIG_WITH_CREDENTIALS, True)
        self._test_bool_env_method("_is_credentials_set_up", env, config_mocks.CONFIG_PARTIAL_CREDENTIALS, False)

        env = TestEnvironment.EnvironmentCredentialsNotRequired()
        self._test_bool_env_method("_is_credentials_set_up", env, config_mocks.CONFIG_STANDARD_ENV, False)

    def _test_bool_env_method(self, method_name: str, env: Environment, config: Dict, expected_result: bool):
        env._config = EnvironmentConfig.get_from_json(json.dumps(config))
        method = getattr(env, method_name)
        if expected_result:
            self.assertTrue(method())
        else:
            self.assertFalse(method())
