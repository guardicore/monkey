from dataclasses import dataclass, field

from marshmallow import fields, validate
from marshmallow_enum import EnumField

from . import CredentialComponentType, ICredentialComponent
from .credential_component_schema import CredentialComponentSchema


class UsernameSchema(CredentialComponentSchema):
    credential_type = EnumField(
        CredentialComponentType, validate=validate.Equal(CredentialComponentType.USERNAME)
    )
    username = fields.Str()


@dataclass(frozen=True)
class Username(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.USERNAME, init=False
    )
    username: str
