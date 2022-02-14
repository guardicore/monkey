from ..credential_types import CredentialTypes

from .i_credential_component import ICredentialComponent


class Username(ICredentialComponent):
    def __init__(self, content: dict):
        super().__init__(type=CredentialTypes.USERNAME, content=content)
