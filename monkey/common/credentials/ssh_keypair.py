from typing import Optional

from pydantic import SecretStr

from ..base_models import InfectionMonkeyBaseModel


class SSHKeypair(InfectionMonkeyBaseModel):
    private_key: SecretStr
    public_key: Optional[str]

    def __hash__(self) -> int:
        return hash((self.private_key, self.public_key))
