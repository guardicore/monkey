import logging

from monkeyevents import CredentialsStolenEvent

from monkey_island.cc.repositories import ICredentialsRepository

logger = logging.getLogger(__name__)


class save_stolen_credentials_to_repository:
    """
    Accepts CredentialsStolenEvent and pushes the stolen credentials into ICredentialsRepository
    """

    def __init__(self, credentials_repository: ICredentialsRepository):
        self._credentials_repository = credentials_repository

    def __call__(self, event: CredentialsStolenEvent):
        self._credentials_repository.save_stolen_credentials(event.stolen_credentials)
