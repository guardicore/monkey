from dataclasses import dataclass, field

from . import CredentialComponentType, ICredentialComponent


@dataclass(frozen=True)
class LMHash(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.LM_HASH, init=False
    )
    lm_hash: str
