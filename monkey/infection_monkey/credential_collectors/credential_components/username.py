from ..credential_type import CredentialType
from .i_credential_component import ICredentialComponent


class Username(ICredentialComponent):
    def __init__(self, username: str):
        super().__init__(type=CredentialType.USERNAME)
        self.username = username
