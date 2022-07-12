from __future__ import annotations

from typing import Dict


class UserCredentials:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def __bool__(self) -> bool:
        return bool(self.username and self.password_hash)

    def to_dict(self) -> Dict:
        cred_dict = {}
        if self.username:
            cred_dict.update({"user": self.username})
        if self.password_hash:
            cred_dict.update({"password_hash": self.password_hash})
        return cred_dict
