from typing import Mapping

from .i_credentials_store import ICredentialsStore


class CredentialsStore(ICredentialsStore):
    def __init__(self, credentials: Mapping = None):
        self.stored_credentials = credentials

    def add_credentials(self, credentials_to_add: Mapping) -> None:
        if self.stored_credentials is None:
            self.stored_credentials = {}

        for key, value in credentials_to_add.items():
            if key not in self.stored_credentials:
                self.stored_credentials[key] = []

            if key != "exploit_ssh_keys":
                self.stored_credentials[key] = list(
                    sorted(set(self.stored_credentials[key]).union(credentials_to_add[key]))
                )
            else:
                self.stored_credentials[key] += credentials_to_add[key]
                self.stored_credentials[key] = [
                    dict(s) for s in set(frozenset(d.items()) for d in self.stored_credentials[key])
                ]

    def get_credentials(self) -> Mapping:
        return self.stored_credentials
