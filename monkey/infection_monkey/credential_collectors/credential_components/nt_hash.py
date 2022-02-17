from dataclasses import dataclass, field

from common.common_consts.credentials_type import CredentialsType
from infection_monkey.i_puppet import ICredentialComponent


@dataclass(frozen=True)
class NTHash(ICredentialComponent):
    credential_type: CredentialsType = field(default=CredentialsType.NT_HASH, init=False)
    nt_hash: str
