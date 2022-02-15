from typing import Iterable

from .credential_components.i_credential_component import ICredentialComponent


class Credentials:
    def __init__(
        self, identities: Iterable[ICredentialComponent], secrets: Iterable[ICredentialComponent]
    ):
        self.identities = tuple(identities)
        self.secrets = tuple(secrets)
