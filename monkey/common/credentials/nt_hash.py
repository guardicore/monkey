import re

from pydantic import validator

from ..base_models import InfectionMonkeyBaseModel
from .validators import ntlm_hash_regex


class NTHash(InfectionMonkeyBaseModel):
    nt_hash: str

    @validator("nt_hash")
    def validate_hash_format(cls, nt_hash):
        if not re.match(ntlm_hash_regex, nt_hash):
            raise ValueError(f"Invalid nt hash provided: {nt_hash}")
        return nt_hash
