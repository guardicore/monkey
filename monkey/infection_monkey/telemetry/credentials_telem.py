from typing import Iterable

from common.common_consts.telem_categories import TelemCategoryEnum
from common.credentials import Credentials
from infection_monkey.telemetry.base_telem import BaseTelem


class CredentialsTelem(BaseTelem):
    telem_category = TelemCategoryEnum.CREDENTIALS

    def __init__(self, credentials: Iterable[Credentials]):
        """
        Used to send information about stolen or discovered credentials to the Island.
        :param credentials: An iterable containing credentials to be sent to the Island.
        """
        self._credentials = credentials

    @property
    def credentials(self) -> Iterable[Credentials]:
        return iter(self._credentials)

    def send(self, log_data=True):
        super().send(log_data=False)

    def get_data(self):
        return [c.dict(simplify=True) for c in self._credentials]
