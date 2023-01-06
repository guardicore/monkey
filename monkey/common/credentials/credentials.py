from __future__ import annotations

from typing import Optional, Union

from ..base_models import InfectionMonkeyBaseModel, InfectionMonkeyModelConfig
from . import LMHash, NTHash, Password, SSHKeypair, Username
from .encoding import SecretEncodingConfig

Secret = Union[Password, LMHash, NTHash, SSHKeypair]
Identity = Username


class Credentials(InfectionMonkeyBaseModel):
    """Represents a credential pair (an identity and a secret)"""

    identity: Optional[Identity]
    """Identity part of credentials, like a username or an email"""

    secret: Optional[Secret]
    """Secret part of credentials, like a password or a hash"""

    def __hash__(self) -> int:
        return hash((self.identity, self.secret))

    class Config(SecretEncodingConfig, InfectionMonkeyModelConfig):
        pass
