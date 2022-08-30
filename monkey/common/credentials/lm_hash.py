from dataclasses import field
from typing import ClassVar

from marshmallow import fields
from pydantic.dataclasses import dataclass

from . import CredentialComponentType, ICredentialComponent
from .credential_component_schema import CredentialComponentSchema, CredentialTypeField
from .validators import credential_component_validator, ntlm_hash_validator


class LMHashSchema(CredentialComponentSchema):
    credential_type = CredentialTypeField(CredentialComponentType.LM_HASH)
    lm_hash = fields.Str(validate=ntlm_hash_validator)


@dataclass
class LMHash(ICredentialComponent):
    credential_type: ClassVar[CredentialComponentType] = field(
        default=CredentialComponentType.LM_HASH, init=False
    )
    lm_hash: str

    def __post_init__(self):
        credential_component_validator(LMHashSchema(), self)
