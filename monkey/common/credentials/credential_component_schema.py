from marshmallow import Schema, post_load, validate
from marshmallow_enum import EnumField

from common.utils.code_utils import del_key

from . import CredentialComponentType


class CredentialTypeField(EnumField):
    def __init__(self, credential_component_type: CredentialComponentType):
        super().__init__(
            CredentialComponentType, validate=validate.Equal(credential_component_type)
        )


class CredentialComponentSchema(Schema):
    @post_load
    def _strip_credential_type(self, data, **kwargs):
        del_key(data, "credential_type")
        return data
