from common.events import CredentialsStolenEvent

from . import IPropagationCredentialsRepository


class add_credentials_from_event_to_propagation_credentials_repository:
    def __init__(self, credentials_repository: IPropagationCredentialsRepository):
        self._credentials_repository = credentials_repository

    def __call__(self, event: CredentialsStolenEvent):
        self._credentials_repository.add_credentials(event.stolen_credentials)
