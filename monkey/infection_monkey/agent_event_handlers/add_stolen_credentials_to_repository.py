import logging

from agentpluginapi import IPropagationCredentialsRepository
from monkeyevents import CredentialsStolenEvent

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
