from ..base_models import InfectionMonkeyBaseModel


class Username(InfectionMonkeyBaseModel):
    username: str

    def __hash__(self):
        return hash(self.username)
