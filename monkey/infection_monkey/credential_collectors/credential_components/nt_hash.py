from dataclasses import dataclass, field

from common.common_consts.credential_component_type import CredentialComponentType
from infection_monkey.i_puppet import ICredentialComponent


@dataclass(frozen=True)
class NTHash(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.NT_HASH, init=False
    )
    nt_hash: str
