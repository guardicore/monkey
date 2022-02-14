from ..credential_types import CredentialTypes

from .i_credential_component import ICredentialComponent


class NtlmHash(ICredentialComponent):
    def __init__(self, content: dict):
        super().__init__(type=CredentialTypes.NTLM_HASH, content=content)
