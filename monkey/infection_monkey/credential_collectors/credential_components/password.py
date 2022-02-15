from dataclasses import dataclass, field

from infection_monkey.i_puppet import CredentialType, ICredentialComponent


@dataclass(frozen=True)
class Password(ICredentialComponent):
    credential_type: CredentialType = field(default=CredentialType.PASSWORD, init=False)
    password: str
