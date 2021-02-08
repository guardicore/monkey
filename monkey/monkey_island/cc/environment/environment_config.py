from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List

import monkey_island.cc.environment.server_config_generator as server_config_generator
from monkey_island.cc.consts import DEFAULT_SERVER_CONFIG_PATH
from monkey_island.cc.environment.user_creds import UserCreds
from monkey_island.cc.resources.auth.auth_user import User
from monkey_island.cc.resources.auth.user_store import UserStore



class EnvironmentConfig:
    def __init__(self,
                 server_config: str,
                 deployment: str,
                 user_creds: UserCreds,
                 aws=None):
        self.server_config_path = None
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
        with open(self.server_config_path, 'w') as f:
            f.write(json.dumps(self.to_dict(), indent=2))

    @staticmethod
    def get_from_file(file_path=DEFAULT_SERVER_CONFIG_PATH) -> EnvironmentConfig:
        file_path = os.path.expanduser(file_path)

        if not Path(file_path).is_file():
            server_config_generator.create_default_config_file(file_path)
        with open(file_path, 'r') as f:
            config_content = f.read()

        environment_config = EnvironmentConfig.get_from_json(config_content)
        # TODO: Populating this property is not ideal. Revisit this when you
        #       make the logger config file configurable at runtime.
        environment_config.server_config_path = file_path

        return environment_config

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
