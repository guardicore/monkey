import logging

import requests

from common.common_consts.timeouts import MEDIUM_REQUEST_TIMEOUT

from . import IslandAPIConnectionError, IslandAPIError, IslandAPITimeoutError

logger = logging.getLogger(__name__)


class IslandAPIClient:
    """
    A client for requests from the Agent to the Island API
    """

    def __init__(self, island_server: str):
        """
        Verifies connection to the Island by raising an error if it can't connect

        :param island_server: Address to the Island
        :raises IslandAPIConnectionError: If a connection cannot be made with the Island
        :raises IslandAPITimeoutError: If a timeout occurs before being able to connect
                                       with the Island
        :raises IslandAPIError: If an unexpected error occurs with the Island API
        """

        try:
            requests.get(  # noqa: DUO123
                f"https://{island_server}/api?action=is-up",
                verify=False,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )
        except requests.exceptions.ConnectionError as err:
            raise IslandAPIConnectionError(err)
        except TimeoutError as err:
            raise IslandAPITimeoutError(err)
        except Exception as err:
            raise IslandAPIError(err)
