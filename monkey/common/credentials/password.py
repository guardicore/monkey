from dataclasses import dataclass, field

from marshmallow import fields, validate
from marshmallow_enum import EnumField

from . import CredentialComponentType, ICredentialComponent
from .credential_component_schema import CredentialComponentSchema


class PasswordSchema(CredentialComponentSchema):
    credential_type = EnumField(
        CredentialComponentType, validate=validate.Equal(CredentialComponentType.PASSWORD)
    )
    password = fields.Str()


@dataclass(frozen=True)
class Password(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.PASSWORD, init=False
    )
    password: str
