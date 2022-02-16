from dataclasses import dataclass, field

from infection_monkey.i_puppet import CredentialType, ICredentialComponent


@dataclass(frozen=True)
class SSHKeypair(ICredentialComponent):
    credential_type: CredentialType = field(default=CredentialType.SSH_KEYPAIR, init=False)
    private_key: str
    public_key: str
