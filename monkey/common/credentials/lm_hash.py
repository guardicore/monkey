import re

from pydantic import SecretStr, validator

from ..base_models import InfectionMonkeyBaseModel
from .validators import ntlm_hash_regex


class LMHash(InfectionMonkeyBaseModel):
    lm_hash: SecretStr

    def __hash__(self) -> int:
        return hash(self.lm_hash)

    @validator("lm_hash")
    def validate_hash_format(cls, lm_hash):
        if not re.match(ntlm_hash_regex, lm_hash.get_secret_value()):
            raise ValueError("Invalid LM hash provided")
        return lm_hash
