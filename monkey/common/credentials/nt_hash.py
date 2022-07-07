from dataclasses import dataclass, field

from marshmallow import fields

from . import CredentialComponentType, ICredentialComponent
from .credential_component_schema import CredentialComponentSchema, CredentialTypeField
from .validators import credential_component_validator, ntlm_hash_validator


class NTHashSchema(CredentialComponentSchema):
    credential_type = CredentialTypeField(CredentialComponentType.NT_HASH)
    nt_hash = fields.Str(validate=ntlm_hash_validator)


@dataclass(frozen=True)
class NTHash(ICredentialComponent):
    credential_type: CredentialComponentType = field(
        default=CredentialComponentType.NT_HASH, init=False
    )
    nt_hash: str

    def __post_init__(self):
        credential_component_validator(NTHashSchema(), self)
