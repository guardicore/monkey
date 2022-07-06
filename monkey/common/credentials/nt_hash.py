from dataclasses import dataclass, field

from . import CredentialComponentType, ICredentialComponent


@dataclass(frozen=True)
class NTHash(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.NT_HASH, init=False
    )
    nt_hash: str
