from typing import Sequence

from monkey_island.cc.repository import ICredentialsRepository
from monkey_island.cc.services.telemetry.processing.credentials import Credentials

fake_username = "m0nk3y_user"
fake_special_username = "m0nk3y.user"
fake_nt_hash = "c1c58f96cdf212b50837bc11a00be47c"
fake_lm_hash = "299BD128C1101FD6"
fake_password_1 = "trytostealthis"
fake_password_2 = "password"
fake_password_3 = "12345678"
PROPAGATION_CREDENTIALS_1 = {
    "identities": [{"username": fake_username, "credential_type": "USERNAME"}],
    "secrets": [
        {"nt_hash": fake_nt_hash, "credential_type": "NT_HASH"},
        {"lm_hash": fake_lm_hash, "credential_type": "LM_HASH"},
        {"password": fake_password_1, "credential_type": "PASSWORD"},
    ],
}

PROPAGATION_CREDENTIALS_2 = {
    "identities": [
        {"username": fake_username, "credential_type": "USERNAME"},
        {"username": fake_special_username, "credential_type": "USERNAME"},
    ],
    "secrets": [
        {"password": fake_password_1, "credential_type": "PASSWORD"},
        {"password": fake_password_2, "credential_type": "PASSWORD"},
        {"password": fake_password_3, "credential_type": "PASSWORD"},
    ],
}


class StubPropagationCredentialsRepository(ICredentialsRepository):
    def get_configured_credentials(self) -> Sequence[Credentials]:
        pass

    def get_stolen_credentials(self) -> Sequence[Credentials]:
        pass

    def get_all_credentials(self) -> Sequence[Credentials]:

        return [
            Credentials.from_mapping(PROPAGATION_CREDENTIALS_1, monkey_guid="some_guid"),
            Credentials.from_mapping(PROPAGATION_CREDENTIALS_2, monkey_guid="second_guid"),
        ]

    def save_configured_credentials(self, credentials: Credentials):
        pass

    def save_stolen_credentials(self, credentials: Credentials):
        pass

    def remove_configured_credentials(self):
        pass

    def remove_stolen_credentials(self):
        pass

    def remove_all_credentials(self):
        pass
