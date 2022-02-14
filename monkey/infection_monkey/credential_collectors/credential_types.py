from enum import Enum


class CredentialTypes(Enum):
    SSH_KEYPAIR = 1
    USERNAME = 2
    PASSWORD = 3
    NTLM_HASH = 4
