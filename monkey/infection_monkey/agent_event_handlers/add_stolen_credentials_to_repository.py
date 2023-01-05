import logging

from common.agent_events import CredentialsStolenEvent
from infection_monkey.propagation_credentials_repository import (
    ILegacyPropagationCredentialsRepository,
    IPropagationCredentialsRepository,
)

logger = logging.getLogger(__name__)


class add_stolen_credentials_to_propagation_credentials_repository:
    def __init__(
        self,
        credentials_repository: IPropagationCredentialsRepository,
        legacy_credentials_repository: ILegacyPropagationCredentialsRepository,
    ):
        self._credentials_repository = credentials_repository
        self._legacy_credentials_repository = legacy_credentials_repository

    def __call__(self, event: CredentialsStolenEvent):
        logger.debug(f"Adding {len(event.stolen_credentials)} to the credentials repository")
        self._credentials_repository.add_credentials(event.stolen_credentials)
        self._legacy_credentials_repository.add_credentials(event.stolen_credentials)
