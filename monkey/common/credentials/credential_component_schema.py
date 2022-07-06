from marshmallow import Schema, post_load

from common.utils.code_utils import del_key


class CredentialComponentSchema(Schema):
    @post_load
    def _strip_credential_type(self, data, **kwargs):
        del_key(data, "credential_type")
        return data
