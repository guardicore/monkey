import logging
import socket
from ipaddress import IPv4Address
from typing import Iterable, Optional

import requests

from common.common_consts.timeouts import MEDIUM_REQUEST_TIMEOUT
from common.network.network_utils import address_to_ip_port
from infection_monkey.network.relay import RELAY_CONTROL_MESSAGE_REMOVE_FROM_WAITLIST
from infection_monkey.utils.threading import create_daemon_thread

logger = logging.getLogger(__name__)


def find_server(servers: Iterable[str]) -> Optional[str]:
    logger.debug(f"Trying to wake up with servers: {', '.join(servers)}")

    for server in servers:
        logger.debug(f"Trying to connect to server: {server}")

        try:
            requests.get(  # noqa: DUO123
                f"https://{server}/api?action=is-up",
                verify=False,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )

            return server
        except requests.exceptions.ConnectionError as err:
            logger.error(f"Unable to connect to server/relay {server}: {err}")
        except TimeoutError as err:
            logger.error(f"Timed out while connecting to server/relay {server}: {err}")
        except Exception as err:
            logger.error(
                f"Exception encountered when trying to connect to server/relay {server}: {err}"
            )

    return None


def send_remove_from_waitlist_control_message_to_relays(servers: Iterable[str]):
    for server in servers:
        t = create_daemon_thread(
            target=_send_remove_from_waitlist_control_message_to_relay,
            name="SendRemoveFromWaitlistControlMessageToRelaysThread",
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
        try:
            d_socket.connect((server_ip, server_port))
            d_socket.sendall(RELAY_CONTROL_MESSAGE_REMOVE_FROM_WAITLIST)
            logger.info(f"Control message was sent to the server/relay {server_ip}:{server_port}")
        except OSError as err:
            logger.error(f"Error connecting to socket {server_ip}:{server_port}: {err}")
