from dataclasses import dataclass, field

from . import CredentialComponentType, ICredentialComponent


@dataclass(frozen=True)
class Password(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.PASSWORD, init=False
    )
    password: str
