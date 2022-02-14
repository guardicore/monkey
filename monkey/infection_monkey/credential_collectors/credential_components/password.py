from ..credential_types import CredentialTypes
from .i_credential_component import ICredentialComponent


class Password(ICredentialComponent):
    def __init__(self, password: str):
        super().__init__(type=CredentialTypes.PASSWORD, content={"password": password})
