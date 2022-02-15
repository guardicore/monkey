from dataclasses import dataclass, field

from ..credential_type import CredentialType
from .i_credential_component import ICredentialComponent


@dataclass(frozen=True)
class LMHash(ICredentialComponent):
    type: CredentialType = field(default=CredentialType.LM_HASH, init=False)
    lm_hash: str
