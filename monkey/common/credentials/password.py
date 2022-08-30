from dataclasses import field
from typing import ClassVar

from marshmallow import fields
from pydantic.dataclasses import dataclass

from . import CredentialComponentType, ICredentialComponent
from .credential_component_schema import CredentialComponentSchema, CredentialTypeField


class PasswordSchema(CredentialComponentSchema):
    credential_type = CredentialTypeField(CredentialComponentType.PASSWORD)
    password = fields.Str()


@dataclass
class Password(ICredentialComponent):
    credential_type: ClassVar[CredentialComponentType] = field(
        default=CredentialComponentType.PASSWORD, init=False
    )
    password: str
