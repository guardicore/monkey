from typing import Dict


class WindowsCredentials:
    def __init__(self, username: str, password="", ntlm_hash="", lm_hash=""):
        self.username = username
        self.password = password
        self.ntlm_hash = ntlm_hash
        self.lm_hash = lm_hash

    def to_dict(self) -> Dict:
        return {'username': self.username,
                'password': self.password,
                'ntlm_hash': self.ntlm_hash,
                'lm_hash': self.lm_hash}
