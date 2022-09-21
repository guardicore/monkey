from __future__ import annotations

from typing import Optional, Union

from pydantic import SecretBytes, SecretStr


def get_plaintext(secret: Union[SecretStr, SecretBytes, None, str]) -> Optional[Union[str, bytes]]:
    if isinstance(secret, (SecretStr, SecretBytes)):
        return secret.get_secret_value()
    else:
        return secret


class SecretEncodingConfig:
    json_encoders = {
        # This makes secrets dumpable to json, but not loggable
        SecretStr: get_plaintext,
        SecretBytes: get_plaintext,
    }
