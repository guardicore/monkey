import json
import os
from unittest import TestCase
from unittest.mock import MagicMock, patch

from monkey_island.cc.consts import MONKEY_ISLAND_ABS_PATH
from common.utils.exceptions import ServerConfigFileChanged
from monkey_island.cc.environment import Environment


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
    CONFIG_JSON_WITH_CREDENTIALS = {
        "server_config": "password",
        "deployment": "develop",
        "user": "test",
        "hash": "9ece086e9bac491fac5c1d1046ca11d737b92a2b2ebd93f005d7b710110c0a678288166e7fbe796883a"
                "4f2e9b3ca9f484f521d0ce464345cc1aec96779149c14"
    }

    CONFIG_JSON_NO_CREDENTIALS = {
        "server_config": "password",
        "deployment": "develop"
    }

    CONFIG_JSON_PARTIAL_CREDENTIALS = {
        "server_config": "password",
        "deployment": "develop",
        "user": "test"
    }

    CONFIG_JSON_STANDARD_ENV = {
        "server_config": "standard",
        "deployment": "develop"
    }

    CONFIG_JSON_STANDARD_WITH_CREDENTIALS = {
        "server_config": "standard",
        "deployment": "develop",
        "user": "test",
        "hash": "9ece086e9bac491fac5c1d1046ca11d737b92a2b2ebd93f005d7b710110c0a678288166e7fbe796883a"
                "4f2e9b3ca9f484f521d0ce464345cc1aec96779149c14"
    }

    @patch.object(target=Environment, attribute="get_server_config_file_path",
                  new=MagicMock(return_value=get_server_config_file_path_test_version()))
    def test_upload_server_configuration_to_file(self):
        Environment.upload_server_configuration_to_file(TestEnvironment.CONFIG_JSON_WITH_CREDENTIALS)
        file_path = get_server_config_file_path_test_version()
        with open(file_path, 'r') as f:
            content_from_file = f.read()
        os.remove(file_path)

        self.assertDictEqual(TestEnvironment.CONFIG_JSON_WITH_CREDENTIALS, json.loads(content_from_file))

    def test_get_server_config_file_path(self):
        server_file_path = MONKEY_ISLAND_ABS_PATH + "\cc/server_config.json"
        self.assertEqual(Environment.get_server_config_file_path(), server_file_path)

    @patch.object(Environment, "upload_server_configuration_to_file", MagicMock())
    def test_set_server_config(self):
        with self.assertRaises(ServerConfigFileChanged):
            Environment.set_server_config(TestEnvironment.CONFIG_JSON_WITH_CREDENTIALS)

    def test_needs_registration(self):
        env = TestEnvironment.EnvironmentWithCredentials()

        env.config = TestEnvironment.CONFIG_JSON_WITH_CREDENTIALS
        self.assertFalse(env.needs_registration())

        env.config = TestEnvironment.CONFIG_JSON_NO_CREDENTIALS
        self.assertTrue(env.needs_registration())

        env.config = TestEnvironment.CONFIG_JSON_PARTIAL_CREDENTIALS
        self.assertTrue(env.needs_registration())

        env = TestEnvironment.EnvironmentNoCredentials()

        env.config = TestEnvironment.CONFIG_JSON_STANDARD_ENV
        self.assertFalse(env.needs_registration())

        env.config = TestEnvironment.CONFIG_JSON_STANDARD_WITH_CREDENTIALS
        self.assertFalse(env.needs_registration())

    def test_is_registered(self):
        env = TestEnvironment.EnvironmentWithCredentials()

        env.config = TestEnvironment.CONFIG_JSON_WITH_CREDENTIALS
        self.assertTrue(env._is_registered())

        env.config = TestEnvironment.CONFIG_JSON_NO_CREDENTIALS
        self.assertFalse(env._is_registered())

        env.config = TestEnvironment.CONFIG_JSON_PARTIAL_CREDENTIALS
        self.assertFalse(env._is_registered())

        env = TestEnvironment.EnvironmentNoCredentials()

        env.config = TestEnvironment.CONFIG_JSON_STANDARD_ENV
        self.assertFalse(env._is_registered())

        env.config = TestEnvironment.CONFIG_JSON_STANDARD_WITH_CREDENTIALS
        self.assertFalse(env._is_registered())

    def test_is_credentials_set_up(self):
        env = TestEnvironment.EnvironmentWithCredentials()

        env.config = TestEnvironment.CONFIG_JSON_NO_CREDENTIALS
        self.assertFalse(env._is_credentials_set_up())

        env.config = TestEnvironment.CONFIG_JSON_WITH_CREDENTIALS
        self.assertTrue(env._is_credentials_set_up())

        env.config = TestEnvironment.CONFIG_JSON_PARTIAL_CREDENTIALS
        self.assertFalse(env._is_credentials_set_up())

        env = TestEnvironment.EnvironmentNoCredentials()

        env.config = TestEnvironment.CONFIG_JSON_STANDARD_ENV
        self.assertFalse(env._is_credentials_set_up())
