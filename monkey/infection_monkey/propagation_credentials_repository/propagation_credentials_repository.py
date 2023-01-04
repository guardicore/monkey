import logging
from itertools import chain
from typing import Iterable, Set

from common.credentials import Credentials
from infection_monkey.i_control_channel import IControlChannel
from infection_monkey.utils.decorators import request_cache

from .i_propagation_credentials_repository import IPropagationCredentialsRepository

logger = logging.getLogger(__name__)

CREDENTIALS_POLL_PERIOD_SEC = 10


class PropagationCredentialsRepository(IPropagationCredentialsRepository):
    """
    Repository that stores credentials on the island and saves/gets credentials by using
    command and control channel
    """

    def __init__(self, control_channel: IControlChannel):
        self._stored_credentials: Set[Credentials] = set()
        self._control_channel = control_channel

        # Ensure caching happens per-instance instead of being shared across instances
        # TODO: Make sure this works in multiprocessing environment
        self._get_credentials_from_control_channel = request_cache(CREDENTIALS_POLL_PERIOD_SEC)(
            self._control_channel.get_credentials_for_propagation
        )

    def add_credentials(self, credentials_to_add: Iterable[Credentials]):
        logger.debug("Adding credentials")
        self._stored_credentials = set(chain(self._stored_credentials, credentials_to_add))

    def get_credentials(self) -> Iterable[Credentials]:
        try:
            propagation_credentials = self._get_credentials_from_control_channel()
            logger.debug(f"Received {len(propagation_credentials)} from the control channel")

            self.add_credentials(propagation_credentials)
        except Exception as ex:
            logger.error(f"Error while attempting to retrieve credentials for propagation: {ex}")

        return self._stored_credentials
