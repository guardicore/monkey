from dataclasses import dataclass, field

from infection_monkey.i_puppet import CredentialType, ICredentialComponent


@dataclass(frozen=True)
class LMHash(ICredentialComponent):
    credential_type: CredentialType = field(default=CredentialType.LM_HASH, init=False)
    lm_hash: str
