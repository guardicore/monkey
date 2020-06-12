from __future__ import annotations

import json
from typing import Dict

from monkey_island.cc.resources.auth.auth_user import User


class UserCreds:

    def __init__(self, username="", password_hash=""):
        self.username = username
        self.password_hash = password_hash

    def __bool__(self) -> bool:
        return bool(self.username and self.password_hash)

    def to_dict(self) -> Dict:
        cred_dict = {}
        if self.username:
            cred_dict.update({'user': self.username})
        if self.password_hash:
            cred_dict.update({'password_hash': self.password_hash})
        return cred_dict

    def to_auth_user(self) -> User:
        return User(1, self.username, self.password_hash)

    @staticmethod
    def get_from_dict(data_dict: Dict) -> UserCreds:
        creds = UserCreds()
        if 'user' in data_dict:
            creds.username = data_dict['user']
        if 'password_hash' in data_dict:
            creds.password_hash = data_dict['password_hash']
        return creds

    @staticmethod
    def get_from_json(json_data: bytes) -> UserCreds:
        cred_dict = json.loads(json_data)
        return UserCreds.get_from_dict(cred_dict)
