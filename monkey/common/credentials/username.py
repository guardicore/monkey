from dataclasses import field
from typing import ClassVar

from marshmallow import fields
from pydantic.dataclasses import dataclass

from . import CredentialComponentType, ICredentialComponent
from .credential_component_schema import CredentialComponentSchema, CredentialTypeField


class UsernameSchema(CredentialComponentSchema):
    credential_type = CredentialTypeField(CredentialComponentType.USERNAME)
    username = fields.Str()


@dataclass
class Username(ICredentialComponent):
    credential_type: ClassVar[CredentialComponentType] = field(
        default=CredentialComponentType.USERNAME, init=False
    )
    username: str
