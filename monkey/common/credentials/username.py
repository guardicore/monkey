from dataclasses import dataclass, field

from marshmallow import Schema, fields, post_load, validate
from marshmallow_enum import EnumField

from common.utils.code_utils import del_key

from . import CredentialComponentType, ICredentialComponent


class UsernameSchema(Schema):
    credential_type = EnumField(
        CredentialComponentType, validate=validate.Equal(CredentialComponentType.USERNAME)
    )
    username = fields.Str()

    @post_load
    def _strip_credential_type(self, data, **kwargs):
        del_key(data, "credential_type")
        return data


@dataclass(frozen=True)
class Username(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.USERNAME, init=False
    )
    username: str
