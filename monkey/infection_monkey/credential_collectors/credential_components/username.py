from ..credential_types import CredentialTypes
from .i_credential_component import ICredentialComponent


class Username(ICredentialComponent):
    def __init__(self, username: str):
        super().__init__(type=CredentialTypes.USERNAME, content={"username": username})
