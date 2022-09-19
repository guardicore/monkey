import logging
import socket
from contextlib import suppress
from ipaddress import IPv4Address
from typing import Dict, Iterable, Iterator, MutableMapping, Optional, Tuple

from common.common_consts.timeouts import LONG_REQUEST_TIMEOUT
from common.network.network_utils import address_to_ip_port
from infection_monkey.island_api_client import (
    HTTPIslandAPIClient,
    IIslandAPIClient,
    IslandAPIConnectionError,
    IslandAPIError,
    IslandAPITimeoutError,
)
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


def find_server(servers: Iterable[str]) -> Tuple[Optional[str], Optional[IIslandAPIClient]]:
    server_list = list(servers)
    server_iterator = ThreadSafeIterator(server_list.__iter__())
    server_results: Dict[str, Tuple[bool, IIslandAPIClient]] = {}

    run_worker_threads(
        _find_island_server,
        "FindIslandServer",
        args=(server_iterator, server_results),
        num_workers=NUM_FIND_SERVER_WORKERS,
    )

    for server in server_list:
        if server_results[server]:
            island_api_client = server_results[server]
            return server, island_api_client

    return (None, None)


def _find_island_server(
    servers: Iterator[str], server_status: MutableMapping[str, Optional[IIslandAPIClient]]
):
    with suppress(StopIteration):
        server = next(servers)
        server_status[server] = _check_if_island_server(server)


def _check_if_island_server(server: str) -> IIslandAPIClient:
    logger.debug(f"Trying to connect to server: {server}")

    try:
        return HTTPIslandAPIClient(server)
    except IslandAPIConnectionError as err:
        logger.error(f"Unable to connect to server/relay {server}: {err}")
    except IslandAPITimeoutError as err:
        logger.error(f"Timed out while connecting to server/relay {server}: {err}")
    except IslandAPIError as err:
        logger.error(
            f"Exception encountered when trying to connect to server/relay {server}: {err}"
        )

    return None


def send_remove_from_waitlist_control_message_to_relays(servers: Iterable[str]):
    for i, server in enumerate(servers, start=1):
        t = create_daemon_thread(
            target=_send_remove_from_waitlist_control_message_to_relay,
            name=f"SendRemoveFromWaitlistControlMessageToRelaysThread-{i:02d}",
            args=(server,),
        )
        t.start()


def _send_remove_from_waitlist_control_message_to_relay(server: str):
    ip, port = address_to_ip_port(server)
    notify_disconnect(IPv4Address(ip), int(port))


def notify_disconnect(server_ip: IPv4Address, server_port: int):
    """
    Tell upstream relay that we no longer need the relay.

    :param server_ip: The IP address of the server to notify.
    :param server_port: The port of the server to notify.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d_socket:
        d_socket.settimeout(LONG_REQUEST_TIMEOUT)

        try:
            d_socket.connect((server_ip, server_port))
            d_socket.sendall(RELAY_CONTROL_MESSAGE_REMOVE_FROM_WAITLIST)
            logger.info(f"Control message was sent to the server/relay {server_ip}:{server_port}")
        except OSError as err:
            logger.error(f"Error connecting to socket {server_ip}:{server_port}: {err}")
