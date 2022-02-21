from dataclasses import dataclass, field

from common.common_consts.credentials_type import CredentialsType
from infection_monkey.i_puppet import ICredentialComponent


@dataclass(frozen=True)
class Password(ICredentialComponent):
    credential_type: CredentialsType = field(default=CredentialsType.PASSWORD.value, init=False)
    password: str
