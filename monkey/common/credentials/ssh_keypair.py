from pydantic import SecretStr

from ..base_models import InfectionMonkeyBaseModel


class SSHKeypair(InfectionMonkeyBaseModel):
    private_key: SecretStr
    public_key: str
