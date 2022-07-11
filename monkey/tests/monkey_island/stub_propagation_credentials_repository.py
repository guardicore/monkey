from typing import Sequence

from tests.data_for_tests.propagation_credentials import (
    PROPAGATION_CREDENTIALS_1,
    PROPAGATION_CREDENTIALS_2,
)

from common.credentials import Credentials
from monkey_island.cc.repository import ICredentialsRepository


class StubPropagationCredentialsRepository(ICredentialsRepository):
    def get_configured_credentials(self) -> Sequence[Credentials]:
        pass

    def get_stolen_credentials(self) -> Sequence[Credentials]:
        return [PROPAGATION_CREDENTIALS_1, PROPAGATION_CREDENTIALS_2]

    def get_all_credentials(self) -> Sequence[Credentials]:

        return [PROPAGATION_CREDENTIALS_1, PROPAGATION_CREDENTIALS_2]

    def save_configured_credentials(self, credentials: Sequence[Credentials]):
        pass

    def save_stolen_credentials(self, credentials: Sequence[Credentials]):
        pass

    def remove_configured_credentials(self):
        pass

    def remove_stolen_credentials(self):
        pass

    def remove_all_credentials(self):
        pass
