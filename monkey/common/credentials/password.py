from pydantic import SecretStr

from ..base_models import InfectionMonkeyBaseModel


class Password(InfectionMonkeyBaseModel):
    password: SecretStr
