from dataclasses import dataclass, field

from ..credential_type import CredentialType
from .i_credential_component import ICredentialComponent


@dataclass(frozen=True)
class Username(ICredentialComponent):
    type: CredentialType = field(default=CredentialType.USERNAME, init=False)
    username: str
