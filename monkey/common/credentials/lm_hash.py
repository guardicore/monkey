from dataclasses import dataclass, field

from marshmallow import fields

from . import CredentialComponentType, ICredentialComponent
from .credential_component_schema import CredentialComponentSchema, CredentialTypeField
from .validators import ntlm_hash_validator


class LMHashSchema(CredentialComponentSchema):
    credential_type = CredentialTypeField(CredentialComponentType.LM_HASH)
    lm_hash = fields.Str(validate=ntlm_hash_validator)


@dataclass(frozen=True)
class LMHash(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.LM_HASH, init=False
    )
    lm_hash: str
