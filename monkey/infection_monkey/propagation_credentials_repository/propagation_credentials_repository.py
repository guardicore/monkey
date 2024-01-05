import logging
import time
from itertools import chain
from multiprocessing import get_context
from multiprocessing.managers import SyncManager
from typing import Iterable

from monkeytypes import Credentials

from infection_monkey.island_api_client import IIslandAPIClient

from .i_propagation_credentials_repository import IPropagationCredentialsRepository

logger = logging.getLogger(__name__)

CREDENTIALS_POLL_PERIOD_SEC = 10


# TODO: See if we can use a multiprocessing proxy object and pass that to plugins instead of this
#       object. That would allow this object to be ignorant of multiprocessing.
class PropagationCredentialsRepository(IPropagationCredentialsRepository):
    """
    Repository that stores credentials on the island and saves/gets credentials by using
    command and control channel
    """

    def __init__(
        self,
        island_api_client: IIslandAPIClient,
        manager: SyncManager,
        polling_period: float = CREDENTIALS_POLL_PERIOD_SEC,
    ):
        self._island_api_client = island_api_client
        self._polling_period = polling_period
        context = get_context("spawn")
        self._lock = context.Lock()
        self._next_update_time = context.Value("d", 0, lock=False)
        self._stored_credentials = manager.list()

    def add_credentials(self, credentials_to_add: Iterable[Credentials]):
        logger.debug("Adding credentials")
        self._stored_credentials.extend(set(chain(self._stored_credentials, credentials_to_add)))

    def get_credentials(self) -> Iterable[Credentials]:
        # TODO: If we can't use a proxy object, consider contributing a multiprocessing-safe
        #       implementation of EggTimer to clean this up.
        #
        #       If we can use a proxy object, we should use
        #       request_cache from monkeytoolbox to decorate this method.
        try:
            with self._lock:
                now = time.monotonic()
                if self._next_update_time.value < now:
                    propagation_credentials = (
                        self._island_api_client.get_credentials_for_propagation()
                    )
                    self._next_update_time.value = time.monotonic() + self._polling_period
                    logger.debug(
                        f"Received {len(propagation_credentials)} from the control channel"
                    )

                    self.add_credentials(propagation_credentials)
        except Exception as ex:
            logger.error(f"Error while attempting to retrieve credentials for propagation: {ex}")

        return self._stored_credentials
