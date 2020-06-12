import json
import os
from typing import Dict
from unittest import TestCase
from unittest.mock import patch, MagicMock

from common.utils.exceptions import InvalidRegistrationCredentials
from monkey_island.cc.environment import Environment, EnvironmentConfig, UserCreds


def get_server_config_file_path_test_version():
    return os.path.join(os.getcwd(), 'test_config.json')


class TestEnvironment(TestCase):

    class EnvironmentNoCredentials(Environment):
        _credentials_required = False

        def get_auth_users(self):
            return []

    class EnvironmentWithCredentials(Environment):
        _credentials_required = True

        def get_auth_users(self):
            return []

    # Username:test Password:test
    CONFIG_WITH_CREDENTIALS = {
        "server_config": "password",
        "deployment": "develop",
        "user": "test",
        "password_hash": "9ece086e9bac491fac5c1d1046ca11d737b92a2b2ebd93f005d7b710110c0a678288166e7fbe796883a"
                "4f2e9b3ca9f484f521d0ce464345cc1aec96779149c14"
    }

    CONFIG_NO_CREDENTIALS = {
        "server_config": "password",
        "deployment": "develop"
    }

    CONFIG_PARTIAL_CREDENTIALS = {
        "server_config": "password",
        "deployment": "develop",
        "user": "test"
    }

    CONFIG_STANDARD_ENV = {
        "server_config": "standard",
        "deployment": "develop"
    }

    CONFIG_STANDARD_WITH_CREDENTIALS = {
        "server_config": "standard",
        "deployment": "develop",
        "user": "test",
        "password_hash": "9ece086e9bac491fac5c1d1046ca11d737b92a2b2ebd93f005d7b710110c0a678288166e7fbe796883a"
                "4f2e9b3ca9f484f521d0ce464345cc1aec96779149c14"
    }

    @patch.object(target=EnvironmentConfig, attribute="save_to_file", new=MagicMock())
    def test_try_add_user(self):
        env = TestEnvironment.EnvironmentWithCredentials()
        credentials = UserCreds(username="test", password_hash="1231234")
        env.try_add_user(credentials)

        credentials = UserCreds(username="test")
        with self.assertRaises(InvalidRegistrationCredentials):
            env.try_add_user(credentials)

        env = TestEnvironment.EnvironmentNoCredentials()
        credentials = UserCreds(username="test", password_hash="1231234")
        with self.assertRaises(InvalidRegistrationCredentials):
            env.try_add_user(credentials)

    def test_needs_registration(self):
        env = TestEnvironment.EnvironmentWithCredentials()
        self._test_bool_env_method("needs_registration", env, TestEnvironment.CONFIG_WITH_CREDENTIALS, False)
        self._test_bool_env_method("needs_registration", env, TestEnvironment.CONFIG_NO_CREDENTIALS, True)
        self._test_bool_env_method("needs_registration", env, TestEnvironment.CONFIG_PARTIAL_CREDENTIALS, True)

        env = TestEnvironment.EnvironmentNoCredentials()
        self._test_bool_env_method("needs_registration", env, TestEnvironment.CONFIG_STANDARD_ENV, False)
        self._test_bool_env_method("needs_registration", env, TestEnvironment.CONFIG_STANDARD_WITH_CREDENTIALS, False)

    def test_is_registered(self):
        env = TestEnvironment.EnvironmentWithCredentials()
        self._test_bool_env_method("_is_registered", env, TestEnvironment.CONFIG_WITH_CREDENTIALS, True)
        self._test_bool_env_method("_is_registered", env, TestEnvironment.CONFIG_NO_CREDENTIALS, False)
        self._test_bool_env_method("_is_registered", env, TestEnvironment.CONFIG_PARTIAL_CREDENTIALS, False)

        env = TestEnvironment.EnvironmentNoCredentials()
        self._test_bool_env_method("_is_registered", env, TestEnvironment.CONFIG_STANDARD_ENV, False)
        self._test_bool_env_method("_is_registered", env, TestEnvironment.CONFIG_STANDARD_WITH_CREDENTIALS, False)

    def test_is_credentials_set_up(self):
        env = TestEnvironment.EnvironmentWithCredentials()
        self._test_bool_env_method("_is_credentials_set_up", env, TestEnvironment.CONFIG_NO_CREDENTIALS, False)
        self._test_bool_env_method("_is_credentials_set_up", env, TestEnvironment.CONFIG_WITH_CREDENTIALS, True)
        self._test_bool_env_method("_is_credentials_set_up", env, TestEnvironment.CONFIG_PARTIAL_CREDENTIALS, False)

        env = TestEnvironment.EnvironmentNoCredentials()
        self._test_bool_env_method("_is_credentials_set_up", env, TestEnvironment.CONFIG_STANDARD_ENV, False)

    def _test_bool_env_method(self, method_name: str, env: Environment, config: Dict, expected_result: bool):
        env._config = EnvironmentConfig.get_from_json(json.dumps(config))
        method = getattr(env, method_name)
        if expected_result:
            self.assertTrue(method())
        else:
            self.assertFalse(method())

