from enum import Enum


class CredentialType(Enum):
    SSH_KEYPAIR = 1
    USERNAME = 2
    PASSWORD = 3
    NTLM_HASH = 4
