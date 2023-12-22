import logging

from monkeyevents import CredentialsStolenEvent

from infection_monkey.propagation_credentials_repository import IPropagationCredentialsRepository

logger = logging.getLogger(__name__)


class add_stolen_credentials_to_propagation_credentials_repository:
    def __init__(
        self,
        credentials_repository: IPropagationCredentialsRepository,
    ):
        self._credentials_repository = credentials_repository

    def __call__(self, event: CredentialsStolenEvent):
        logger.debug(f"Adding {len(event.stolen_credentials)} to the credentials repository")
        self._credentials_repository.add_credentials(event.stolen_credentials)
