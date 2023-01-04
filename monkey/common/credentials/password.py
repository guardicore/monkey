from pydantic import SecretStr

from ..base_models import InfectionMonkeyBaseModel


class Password(InfectionMonkeyBaseModel):
    password: SecretStr

    def __hash__(self):
        return hash(self.password)
