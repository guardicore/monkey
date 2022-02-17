from enum import Enum


class CredentialsType(Enum):
    USERNAME = 1
    PASSWORD = 2
    NT_HASH = 3
    LM_HASH = 4
    SSH_KEYPAIR = 5
