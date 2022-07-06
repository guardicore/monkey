from dataclasses import dataclass, field

from marshmallow import fields

from . import CredentialComponentType, ICredentialComponent
from .credential_component_schema import CredentialComponentSchema, CredentialTypeField


class PasswordSchema(CredentialComponentSchema):
    credential_type = CredentialTypeField(CredentialComponentType.PASSWORD)
    password = fields.Str()


@dataclass(frozen=True)
class Password(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.PASSWORD, init=False
    )
    password: str
