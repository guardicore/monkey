from ..credential_type import CredentialType
from .i_credential_component import ICredentialComponent


class LMHash(ICredentialComponent):
    def __init__(self, lm_hash: str):
        super().__init__(type=CredentialType.NTLM_HASH, content={"lm_hash": lm_hash})
