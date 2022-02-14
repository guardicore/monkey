from ..credential_types import CredentialTypes
from .i_credential_component import ICredentialComponent


class SSHKeypair(ICredentialComponent):
    def __init__(self, content: dict):
        super().__init__(type=CredentialTypes.SSH_KEYPAIR, content=content)
