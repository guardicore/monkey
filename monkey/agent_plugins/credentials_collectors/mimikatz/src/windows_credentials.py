from typing import Dict


class WindowsCredentials:
    def __init__(self, username: str, password="", ntlm_hash="", lm_hash=""):
        self.username = username
        self.password = password
        self.ntlm_hash = ntlm_hash
        self.lm_hash = lm_hash

    def to_dict(self) -> Dict[str, str]:
        return {
            "username": self.username,
            "password": self.password,
            "ntlm_hash": self.ntlm_hash,
            "lm_hash": self.lm_hash,
        }

    def __eq__(self, other):
        if isinstance(other, WindowsCredentials):
            return (
                self.username == other.username
                and self.password == other.password
                and self.ntlm_hash == other.ntlm_hash
                and self.lm_hash == other.lm_hash
            )
        return False

    def __hash__(self):
        return hash((self.username, self.password, self.ntlm_hash, self.lm_hash))
