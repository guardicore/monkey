import json
import os
import platform
from typing import Dict
from unittest import TestCase
from unittest.mock import MagicMock, patch

import monkey_island.cc.testing.environment.server_config_mocks as config_mocks
from monkey_island.cc.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.environment.environment_config import EnvironmentConfig
from monkey_island.cc.environment.user_creds import UserCreds


def get_server_config_file_path_test_version():
    return os.path.join(os.getcwd(), 'test_config.json')


class TestEnvironmentConfig(TestCase):

    def test_get_from_json(self):
        self._test_get_from_json(config_mocks.CONFIG_WITH_CREDENTIALS)
        self._test_get_from_json(config_mocks.CONFIG_NO_CREDENTIALS)
        self._test_get_from_json(config_mocks.CONFIG_PARTIAL_CREDENTIALS)

    def _test_get_from_json(self, config: Dict):
        config_json = json.dumps(config)
        env_config_object = EnvironmentConfig.get_from_json(config_json)
        self.assertEqual(config['server_config'], env_config_object.server_config)
        self.assertEqual(config['deployment'], env_config_object.deployment)
        if 'user' in config:
            self.assertEqual(config['user'], env_config_object.user_creds.username)
        if 'password_hash' in config:
            self.assertEqual(config['password_hash'], env_config_object.user_creds.password_hash)
        if 'aws' in config:
            self.assertEqual(config['aws'], env_config_object.aws)

    def test_save_to_file(self):
        self._test_save_to_file(config_mocks.CONFIG_WITH_CREDENTIALS)
        self._test_save_to_file(config_mocks.CONFIG_NO_CREDENTIALS)
        self._test_save_to_file(config_mocks.CONFIG_PARTIAL_CREDENTIALS)

    @patch.object(target=EnvironmentConfig, attribute="get_config_file_path",
                  new=MagicMock(return_value=get_server_config_file_path_test_version()))
    def _test_save_to_file(self, config: Dict):
        user_creds = UserCreds.get_from_dict(config)
        env_config = EnvironmentConfig(server_config=config['server_config'],
                                       deployment=config['deployment'],
                                       user_creds=user_creds)

        env_config.save_to_file()
        file_path = get_server_config_file_path_test_version()
        with open(file_path, 'r') as f:
            content_from_file = f.read()
        os.remove(file_path)

        self.assertDictEqual(config, json.loads(content_from_file))

    def test_get_server_config_file_path(self):
        if platform.system() == "Windows":
            server_file_path = MONKEY_ISLAND_ABS_PATH + r"\cc\server_config.json"
        else:
            server_file_path = MONKEY_ISLAND_ABS_PATH + "/cc/server_config.json"
        self.assertEqual(EnvironmentConfig.get_config_file_path(), server_file_path)

    def test_get_from_dict(self):
        config_dict = config_mocks.CONFIG_WITH_CREDENTIALS
        env_conf = EnvironmentConfig.get_from_dict(config_dict)
        self.assertEqual(env_conf.server_config, config_dict['server_config'])
        self.assertEqual(env_conf.deployment, config_dict['deployment'])
        self.assertEqual(env_conf.user_creds.username, config_dict['user'])
        self.assertEqual(env_conf.aws, None)

        config_dict = config_mocks.CONFIG_BOGUS_VALUES
        env_conf = EnvironmentConfig.get_from_dict(config_dict)
        self.assertEqual(env_conf.server_config, config_dict['server_config'])
        self.assertEqual(env_conf.deployment, config_dict['deployment'])
        self.assertEqual(env_conf.user_creds.username, config_dict['user'])
        self.assertEqual(env_conf.aws, config_dict['aws'])

    def test_to_dict(self):
        conf_json1 = json.dumps(config_mocks.CONFIG_WITH_CREDENTIALS)
        self._test_to_dict(EnvironmentConfig.get_from_json(conf_json1))

        conf_json2 = json.dumps(config_mocks.CONFIG_NO_CREDENTIALS)
        self._test_to_dict(EnvironmentConfig.get_from_json(conf_json2))

        conf_json3 = json.dumps(config_mocks.CONFIG_PARTIAL_CREDENTIALS)
        self._test_to_dict(EnvironmentConfig.get_from_json(conf_json3))

    def _test_to_dict(self, env_config_object: EnvironmentConfig):
        test_dict = {'server_config': env_config_object.server_config,
                     'deployment': env_config_object.deployment}
        user_creds = env_config_object.user_creds
        if user_creds.username:
            test_dict.update({'user': user_creds.username})
        if user_creds.password_hash:
            test_dict.update({'password_hash': user_creds.password_hash})

        self.assertDictEqual(test_dict, env_config_object.to_dict())
