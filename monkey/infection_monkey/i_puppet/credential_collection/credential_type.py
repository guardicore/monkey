from enum import Enum


class CredentialType(Enum):
    USERNAME = 2
    PASSWORD = 3
    NT_HASH = 4
    LM_HASH = 5
