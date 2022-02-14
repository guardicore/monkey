from dataclasses import dataclass
from typing import List

from .credential_components.i_credential_component import ICredentialComponent


@dataclass
class Credentials:
    identities: List[ICredentialComponent]
    secrets: List[ICredentialComponent]
