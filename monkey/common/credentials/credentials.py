from __future__ import annotations

from typing import Optional, Union

from pydantic import SecretBytes, SecretStr

from ..base_models import InfectionMonkeyBaseModel
from . import LMHash, NTHash, Password, SSHKeypair, Username

Secret = Union[Password, LMHash, NTHash, SSHKeypair]
Identity = Username


def get_plaintext(secret: Union[SecretStr, SecretBytes, None, str]) -> Optional[str]:
    if isinstance(secret, (SecretStr, SecretBytes)):
        return secret.get_secret_value()
    else:
        return secret


class Credentials(InfectionMonkeyBaseModel):
    """Represents a credential pair (some form of identity and a secret)"""

    identity: Optional[Identity]
    """Identity part of credentials, like a username or an email"""

    secret: Optional[Secret]
    """Secret part of credentials, like a password or a hash"""

    class Config:
        json_encoders = {
            # This makes secrets dumpable to json, but not loggable
            SecretStr: lambda v: v.get_secret_value() if v else None,
            SecretBytes: lambda v: v.get_secret_value() if v else None,
        }
