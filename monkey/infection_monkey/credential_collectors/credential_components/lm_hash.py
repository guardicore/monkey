from dataclasses import dataclass, field

from common.common_consts.credentials_type import CredentialsType
from infection_monkey.i_puppet import ICredentialComponent


@dataclass(frozen=True)
class LMHash(ICredentialComponent):
    credential_type: CredentialsType = field(default=CredentialsType.LM_HASH, init=False)
    lm_hash: str
