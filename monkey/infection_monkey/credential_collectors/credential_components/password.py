from ..credential_type import CredentialType
from .i_credential_component import ICredentialComponent


class Password(ICredentialComponent):
    def __init__(self, password: str):
        super().__init__(type=CredentialType.PASSWORD, content={"password": password})
