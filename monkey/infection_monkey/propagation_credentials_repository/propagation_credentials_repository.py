import logging
import time
from itertools import chain
from multiprocessing import get_context
from typing import Iterable

from common.credentials import Credentials
from infection_monkey.i_control_channel import IControlChannel

from .i_propagation_credentials_repository import IPropagationCredentialsRepository

logger = logging.getLogger(__name__)

CREDENTIALS_POLL_PERIOD_SEC = 10


class PropagationCredentialsRepository(IPropagationCredentialsRepository):
    """
    Repository that stores credentials on the island and saves/gets credentials by using
    command and control channel
    """

    def __init__(self, control_channel: IControlChannel):
        self._control_channel = control_channel
        context = get_context("spawn")
        self._next_update_time = context.Value("d", 0)
        self._stored_credentials = context.Manager().list()

    def add_credentials(self, credentials_to_add: Iterable[Credentials]):
        logger.debug("Adding credentials")
        self._stored_credentials.extend(set(chain(self._stored_credentials, credentials_to_add)))

    def get_credentials(self) -> Iterable[Credentials]:
        try:
            with self._next_update_time.get_lock():
                now = time.monotonic()
                if self._next_update_time.value < now:
                    propagation_credentials = (
                        self._control_channel.get_credentials_for_propagation()
                    )
                    self._next_update_time.value = time.monotonic() + CREDENTIALS_POLL_PERIOD_SEC
                    logger.debug(
                        f"Received {len(propagation_credentials)} from the control channel"
                    )

                    self.add_credentials(propagation_credentials)
        except Exception as ex:
            logger.error(f"Error while attempting to retrieve credentials for propagation: {ex}")

        return self._stored_credentials
