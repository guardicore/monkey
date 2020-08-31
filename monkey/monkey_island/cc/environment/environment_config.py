from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List

import monkey_island.cc.environment.server_config_generator as server_config_generator
from monkey_island.cc.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.environment.user_creds import UserCreds
from monkey_island.cc.resources.auth.auth_user import User
from monkey_island.cc.resources.auth.user_store import UserStore

SERVER_CONFIG_FILENAME = "server_config.json"


class EnvironmentConfig:
    def __init__(self,
                 server_config: str,
                 deployment: str,
                 user_creds: UserCreds,
                 aws=None):
        self.server_config = server_config
        self.deployment = deployment
        self.user_creds = user_creds
        self.aws = aws

    @staticmethod
    def get_from_json(config_json: str) -> EnvironmentConfig:
        data = json.loads(config_json)
        return EnvironmentConfig.get_from_dict(data)

    @staticmethod
    def get_from_dict(dict_data: Dict) -> EnvironmentConfig:
        user_creds = UserCreds.get_from_dict(dict_data)
        aws = dict_data['aws'] if 'aws' in dict_data else None
        return EnvironmentConfig(server_config=dict_data['server_config'],
                                 deployment=dict_data['deployment'],
                                 user_creds=user_creds,
                                 aws=aws)

    def save_to_file(self):
        file_path = EnvironmentConfig.get_config_file_path()
        with open(file_path, 'w') as f:
            f.write(json.dumps(self.to_dict(), indent=2))

    @staticmethod
    def get_from_file() -> EnvironmentConfig:
        file_path = EnvironmentConfig.get_config_file_path()
        if not Path(file_path).is_file():
            server_config_generator.create_default_config_file(file_path)
        with open(file_path, 'r') as f:
            config_content = f.read()
        return EnvironmentConfig.get_from_json(config_content)

    @staticmethod
    def get_config_file_path() -> str:
        return os.path.join(MONKEY_ISLAND_ABS_PATH, 'cc', SERVER_CONFIG_FILENAME)

    def to_dict(self) -> Dict:
        config_dict = {'server_config': self.server_config,
                       'deployment': self.deployment}
        if self.aws:
            config_dict.update({'aws': self.aws})
        config_dict.update(self.user_creds.to_dict())
        return config_dict

    def add_user(self, credentials: UserCreds):
        self.user_creds = credentials
        self.save_to_file()
        UserStore.set_users(self.get_users())

    def get_users(self) -> List[User]:
        auth_user = self.user_creds.to_auth_user()
        return [auth_user] if auth_user else []
