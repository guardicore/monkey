import re

from marshmallow import validate

_ntlm_hash_regex = re.compile(r"^[a-fA-F0-9]{32}$")
ntlm_hash_validator = validate.Regexp(regex=_ntlm_hash_regex)
