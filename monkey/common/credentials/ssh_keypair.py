from dataclasses import dataclass, field

from marshmallow import fields

from . import CredentialComponentType, ICredentialComponent
from .credential_component_schema import CredentialComponentSchema, CredentialTypeField


class SSHKeypairSchema(CredentialComponentSchema):
    credential_type = CredentialTypeField(CredentialComponentType.SSH_KEYPAIR)
    # TODO: Find a list of valid formats for ssh keys and add validators
    private_key = fields.Str()
    public_key = fields.Str()


@dataclass(frozen=True)
class SSHKeypair(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.SSH_KEYPAIR, init=False
    )
    private_key: str
    public_key: str
