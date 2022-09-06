import re

from pydantic import validator
from pydantic.main import BaseModel

from .validators import ntlm_hash_regex


class LMHash(BaseModel):
    lm_hash: str

    @validator("lm_hash")
    def validate_hash_format(cls, nt_hash):
        if not re.match(ntlm_hash_regex, nt_hash):
            raise ValueError(f"Invalid LM hash provided: {nt_hash}")
        return nt_hash
