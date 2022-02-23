from dataclasses import dataclass, field

from common.common_consts.credential_component_type import CredentialComponentType
from infection_monkey.i_puppet import ICredentialComponent


@dataclass(frozen=True)
class SSHKeypair(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.SSH_KEYPAIR, init=False
    )
    private_key: str
    public_key: str
