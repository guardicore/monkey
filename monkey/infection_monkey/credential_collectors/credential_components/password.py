from dataclasses import dataclass, field

from common.common_consts.credential_component_type import CredentialComponentType
from infection_monkey.i_puppet import ICredentialComponent


@dataclass(frozen=True)
class Password(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.PASSWORD, init=False
    )
    password: str
