from enum import Enum


class CredentialType(Enum):
    USERNAME = 2
    PASSWORD = 3
    NTLM_HASH = 4
