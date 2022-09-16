import logging

import requests

from common.common_consts.timeouts import MEDIUM_REQUEST_TIMEOUT
from infection_monkey.transport.island_api_client_errors import (
    IslandAPIConnectionError,
    IslandAPIError,
    IslandAPITimeoutError,
)

logger = logging.getLogger(__name__)


class IslandApiClient:
    """
    Represents Island API client
    """

    def __init__(self, island_server: str):
        """
        Tries to connect to the island.

        :param island_server: String representing the island ip address and port
        :raises IslandAPIError:
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
