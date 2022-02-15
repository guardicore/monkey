from dataclasses import dataclass
from typing import Tuple

from .i_credential_component import ICredentialComponent


@dataclass(frozen=True)
class Credentials:
    identities: Tuple[ICredentialComponent]
    secrets: Tuple[ICredentialComponent]
