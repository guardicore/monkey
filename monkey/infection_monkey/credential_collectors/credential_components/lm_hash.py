from ..credential_type import CredentialType
from .i_credential_component import ICredentialComponent


class LMHash(ICredentialComponent):
    type = CredentialType.LM_HASH

    def __init__(self, lm_hash: str):
        self.lm_hash = lm_hash
