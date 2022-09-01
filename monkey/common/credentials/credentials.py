from __future__ import annotations

from typing import Optional, Union

from ..base_models import InfectionMonkeyBaseModel
from . import LMHash, NTHash, Password, SSHKeypair, Username

Secret = Union[Password, LMHash, NTHash, SSHKeypair]
Identity = Username


class Credentials(InfectionMonkeyBaseModel):
    identity: Optional[Identity]
    secret: Optional[Secret]
