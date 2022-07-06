from dataclasses import dataclass, field

from . import CredentialComponentType, ICredentialComponent


@dataclass(frozen=True)
class Username(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.USERNAME, init=False
    )
    username: str
