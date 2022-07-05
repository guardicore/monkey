from dataclasses import dataclass, field

from . import CredentialComponentType, ICredentialComponent


@dataclass(frozen=True)
class SSHKeypair(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.SSH_KEYPAIR, init=False
    )
    private_key: str
    public_key: str
