from dataclasses import field
from typing import ClassVar

from marshmallow import fields
from pydantic.dataclasses import dataclass

from . import CredentialComponentType, ICredentialComponent
from .credential_component_schema import CredentialComponentSchema, CredentialTypeField


class SSHKeypairSchema(CredentialComponentSchema):
    credential_type: ClassVar[CredentialComponentType] = CredentialTypeField(
        CredentialComponentType.SSH_KEYPAIR
    )
    # TODO: Find a list of valid formats for ssh keys and add validators.
    #       See https://github.com/nemchik/ssh-key-regex
    private_key = fields.Str()
    public_key = fields.Str()


@dataclass
class SSHKeypair(ICredentialComponent):
    credential_type: ClassVar[CredentialComponentType] = field(
        default=CredentialComponentType.SSH_KEYPAIR, init=False
    )
    private_key: str
    public_key: str
