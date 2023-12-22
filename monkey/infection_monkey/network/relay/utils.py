import logging
import socket
from contextlib import suppress
from typing import Dict, Iterable, Iterator

import requests
from monkeytypes import SocketAddress

from common.common_consts.timeouts import LONG_REQUEST_TIMEOUT, MEDIUM_REQUEST_TIMEOUT
from infection_monkey.network.relay import RELAY_CONTROL_MESSAGE_REMOVE_FROM_WAITLIST
from infection_monkey.utils.threading import (
    ThreadSafeIterator,
    create_daemon_thread,
    run_worker_threads,
)

logger = logging.getLogger(__name__)

# The number of Island servers to test simultaneously. 32 threads seems large enough for all
# practical purposes. Revisit this if it's not.
NUM_FIND_SERVER_WORKERS = 32


IslandAPISearchResults = Dict[SocketAddress, bool]


def find_available_island_apis(servers: Iterable[SocketAddress]) -> IslandAPISearchResults:
    server_list = list(servers)
    server_iterator = ThreadSafeIterator(server_list.__iter__())
    server_results: IslandAPISearchResults = {}

    run_worker_threads(
        _find_island_server,
        "FindIslandServer",
        args=(server_iterator, server_results),
        num_workers=NUM_FIND_SERVER_WORKERS,
    )

    return server_results


def _find_island_server(
    servers: Iterator[SocketAddress],
    server_results: IslandAPISearchResults,
):
    with suppress(StopIteration):
        server = next(servers)
        server_results[server] = _server_is_island(server)


def _server_is_island(server: SocketAddress) -> bool:
    logger.debug(f"Trying to connect to server: {server}")

    try:
        response = requests.get(  # noqa: DUO123
            f"https://{server}/api?action=is-up", verify=False, timeout=MEDIUM_REQUEST_TIMEOUT
        )
        response.raise_for_status()

        logger.debug(f"Successfully connected to the Island via {server}")
        return True
    except requests.exceptions.RequestException as err:
        logger.error(f"Unable to connect to server/relay {server}: {err}")

    return False


def send_remove_from_waitlist_control_message_to_relays(servers: Iterable[SocketAddress]):
    for i, server in enumerate(servers, start=1):
        t = create_daemon_thread(
            target=notify_disconnect,
            name=f"SendRemoveFromWaitlistControlMessageToRelaysThread-{i:02d}",
            args=(server,),
        )
        t.start()


def notify_disconnect(server_address: SocketAddress):
    """
    Tell upstream relay that we no longer need the relay

    :param server_address: The address of the server to notify
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d_socket:
        d_socket.settimeout(LONG_REQUEST_TIMEOUT)

        try:
            d_socket.connect((str(server_address.ip), server_address.port))
            d_socket.sendall(RELAY_CONTROL_MESSAGE_REMOVE_FROM_WAITLIST)
            logger.info(f"Control message was sent to the server/relay {server_address}")
        except OSError as err:
            logger.error(f"Error connecting to socket {server_address}: {err}")
