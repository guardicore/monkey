import functools
import logging

import requests

from common.common_consts.timeouts import LONG_REQUEST_TIMEOUT, MEDIUM_REQUEST_TIMEOUT

from . import IIslandAPIClient, IslandAPIConnectionError, IslandAPIError, IslandAPITimeoutError

logger = logging.getLogger(__name__)


def handle_island_errors(fn):
    @functools.wraps(fn)
    def decorated(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except requests.exceptions.ConnectionError as err:
            raise IslandAPIConnectionError(err)
        except TimeoutError as err:
            raise IslandAPITimeoutError(err)
        except Exception as err:
            raise IslandAPIError(err)

    return decorated


class HTTPIslandAPIClient(IIslandAPIClient):
    """
    A client for the Island's HTTP API
    """

    @handle_island_errors
    def __init__(self, island_server: str):
        requests.get(  # noqa: DUO123
            f"https://{island_server}/api?action=is-up",
            verify=False,
            timeout=MEDIUM_REQUEST_TIMEOUT,
        )

        self._island_server = island_server

    @handle_island_errors
    def send_log(self, log_contents: str):
        requests.post(  # noqa: DUO123
            f"https://{self._island_server}/api/log",
            json=log_contents,
            verify=False,
            timeout=MEDIUM_REQUEST_TIMEOUT,
        )

    @staticmethod
    @handle_island_errors
    def get_pba_file(server_address: str, filename: str):
        return requests.get(  # noqa: DUO123
            "https://%s/api/pba/download/%s" % (server_address, filename),
            verify=False,
            timeout=LONG_REQUEST_TIMEOUT,
        )
