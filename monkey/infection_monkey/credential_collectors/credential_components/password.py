from dataclasses import dataclass, field

from ..credential_type import CredentialType
from .i_credential_component import ICredentialComponent


@dataclass(frozen=True)
class Password(ICredentialComponent):
    type: CredentialType = field(default=CredentialType.PASSWORD, init=False)
    password: str
