from enum import Enum, auto


class CredentialComponentType(Enum):
    USERNAME = auto()
    PASSWORD = auto()
    NT_HASH = auto()
    LM_HASH = auto()
    SSH_KEYPAIR = auto()
