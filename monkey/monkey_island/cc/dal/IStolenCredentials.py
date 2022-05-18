from abc import ABC
from typing import Sequence

from monkey_island.cc.models import StolenCredentials


# Consider removing this interface and just using the telemetry type
class IStolenCredentialsRepository(ABC):
    def get_stolen_credentials(self) -> Sequence[StolenCredentials]:
        pass

    def save_stolen_credentials(self, stolen_credentials: StolenCredentials):
        pass
