from ..credential_type import CredentialType
from .i_credential_component import ICredentialComponent


class NTHash(ICredentialComponent):
    def __init__(self, nt_hash: str):
        super().__init__(type=CredentialType.NTLM_HASH)
        self.nt_hash = nt_hash
