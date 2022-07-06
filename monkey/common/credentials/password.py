from dataclasses import dataclass, field

from marshmallow import Schema, fields, post_load, validate
from marshmallow_enum import EnumField

from common.utils.code_utils import del_key

from . import CredentialComponentType, ICredentialComponent


class PasswordSchema(Schema):
    credential_type = EnumField(
        CredentialComponentType, validate=validate.Equal(CredentialComponentType.PASSWORD)
    )
    password = fields.Str()

    @post_load
    def _strip_credential_type(self, data, **kwargs):
        del_key(data, "credential_type")
        return data


@dataclass(frozen=True)
class Password(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.PASSWORD, init=False
    )
    password: str
