from dataclasses import dataclass, field

from ..credential_type import CredentialType
from .i_credential_component import ICredentialComponent


@dataclass(frozen=True)
class NTHash(ICredentialComponent):
    type: CredentialType = field(default=CredentialType.NT_HASH, init=False)
    nt_hash: str
