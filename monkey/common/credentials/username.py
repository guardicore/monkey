from dataclasses import dataclass, field

from marshmallow import fields

from . import CredentialComponentType, ICredentialComponent
from .credential_component_schema import CredentialComponentSchema, CredentialTypeField


class UsernameSchema(CredentialComponentSchema):
    credential_type = CredentialTypeField(CredentialComponentType.USERNAME)
    username = fields.Str()


@dataclass(frozen=True)
class Username(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.USERNAME, init=False
    )
    username: str
