from ..credential_types import CredentialTypes
from .i_credential_component import ICredentialComponent


class NTHashes(ICredentialComponent):
    def __init__(self, ntlm_hash: str, lm_hash: str):
        super().__init__(
            type=CredentialTypes.NTLM_HASH, content={"ntlm_hash": ntlm_hash, "lm_hash": lm_hash}
        )
