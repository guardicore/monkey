from dataclasses import dataclass, field

from infection_monkey.i_puppet import CredentialType, ICredentialComponent


@dataclass(frozen=True)
class Username(ICredentialComponent):
    credential_type: CredentialType = field(default=CredentialType.USERNAME, init=False)
    username: str
