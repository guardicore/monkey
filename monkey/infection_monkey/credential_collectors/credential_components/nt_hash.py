from ..credential_type import CredentialType
from .i_credential_component import ICredentialComponent


class NTHash(ICredentialComponent):
    type = CredentialType.NT_HASH

    def __init__(self, nt_hash: str):
        self.nt_hash = nt_hash
