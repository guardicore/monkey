from typing import Sequence

from monkeytypes import Credentials

from monkey_island.cc.repositories import ICredentialsRepository


class InMemoryCredentialsRepository(ICredentialsRepository):
    def __init__(self):
        self._configured_credentials = []
        self._stolen_credentials = []

    def get_configured_credentials(self) -> Sequence[Credentials]:
        return self._configured_credentials

    def get_stolen_credentials(self) -> Sequence[Credentials]:
        return self._stolen_credentials

    def get_all_credentials(self) -> Sequence[Credentials]:
        return [*self._configured_credentials, *self._stolen_credentials]

    def save_configured_credentials(self, credentials: Sequence[Credentials]):
        self._configured_credentials.extend(credentials)

    def save_stolen_credentials(self, credentials: Sequence[Credentials]):
        self._stolen_credentials.extend(credentials)

    def remove_configured_credentials(self):
        self._configured_credentials = []

    def remove_stolen_credentials(self):
        self._stolen_credentials = []

    def remove_all_credentials(self):
        self.remove_configured_credentials()
        self.remove_stolen_credentials()

    def reset(self):
        self.remove_all_credentials()
