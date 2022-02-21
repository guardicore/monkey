from dataclasses import dataclass, field

from common.common_consts.credentials_type import CredentialsType
from infection_monkey.i_puppet import ICredentialComponent


@dataclass(frozen=True)
class SSHKeypair(ICredentialComponent):
    credential_type: CredentialsType = field(default=CredentialsType.SSH_KEYPAIR.value, init=False)
    private_key: str
    public_key: str
