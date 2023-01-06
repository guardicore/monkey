import re

from pydantic import SecretStr, validator

from ..base_models import InfectionMonkeyBaseModel
from .validators import ntlm_hash_regex


class NTHash(InfectionMonkeyBaseModel):
    nt_hash: SecretStr

    def __hash__(self) -> int:
        return hash(self.nt_hash)

    @validator("nt_hash")
    def validate_hash_format(cls, nt_hash):
        if not re.match(ntlm_hash_regex, nt_hash.get_secret_value()):
            raise ValueError("Invalid NT hash provided")
        return nt_hash
