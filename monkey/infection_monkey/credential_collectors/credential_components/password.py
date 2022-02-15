from ..credential_type import CredentialType
from .i_credential_component import ICredentialComponent


class Password(ICredentialComponent):
    type = CredentialType.PASSWORD

    def __init__(self, password: str):
        self.password = password
