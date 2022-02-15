from ..credential_type import CredentialType
from .i_credential_component import ICredentialComponent


class Username(ICredentialComponent):
    type = CredentialType.USERNAME

    def __init__(self, username: str):
        self.username = username
