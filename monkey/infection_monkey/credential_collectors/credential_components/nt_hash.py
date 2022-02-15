from dataclasses import dataclass, field

from infection_monkey.i_puppet import CredentialType, ICredentialComponent


@dataclass(frozen=True)
class NTHash(ICredentialComponent):
    credential_type: CredentialType = field(default=CredentialType.NT_HASH, init=False)
    nt_hash: str
