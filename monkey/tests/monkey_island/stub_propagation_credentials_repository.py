from typing import Sequence

from common.credentials import Credentials, LMHash, NTHash, Password, Username
from monkey_island.cc.repository import ICredentialsRepository

fake_username = "m0nk3y_user"
fake_special_username = "m0nk3y.user"
fake_nt_hash = "C1C58F96CDF212B50837BC11A00BE47C"
fake_lm_hash = "299BD128C1101FD6299BD128C1101FD6"
fake_password_1 = "trytostealthis"
fake_password_2 = "password"
fake_password_3 = "12345678"
PROPAGATION_CREDENTIALS_1 = Credentials(
    identities=(Username(fake_username),),
    secrets=(NTHash(fake_nt_hash), LMHash(fake_lm_hash), Password(fake_password_1)),
)
PROPAGATION_CREDENTIALS_2 = Credentials(
    identities=(Username(fake_username), Username(fake_special_username)),
    secrets=(Password(fake_password_1), Password(fake_password_2), Password(fake_password_3)),
)


class StubPropagationCredentialsRepository(ICredentialsRepository):
    def get_configured_credentials(self) -> Sequence[Credentials]:
        pass

    def get_stolen_credentials(self) -> Sequence[Credentials]:
        pass

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
