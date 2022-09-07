import logging
import socket
from typing import Sequence

import requests

from common.common_consts.timeouts import MEDIUM_REQUEST_TIMEOUT
from common.network.network_utils import address_to_ip_port
from infection_monkey.network.relay import RELAY_CONTROL_MESSAGE
from infection_monkey.utils.threading import create_daemon_thread

logger = logging.getLogger(__name__)


def find_server(self, servers: Sequence[str]):
    logger.debug(f"Trying to wake up with servers: {', '.join(servers)}")

    server_iterator = (s for s in servers)
    for server in server_iterator:
        try:
            debug_message = f"Trying to connect to server: {server}"
            logger.debug(debug_message)
            requests.get(  # noqa: DUO123
                f"https://{server}/api?action=is-up",
                verify=False,
                timeout=MEDIUM_REQUEST_TIMEOUT,
            )

            break
        except requests.exceptions.ConnectionError as err:
            logger.error(f"Unable to connect to server/relay {server}: {err}")
        except TimeoutError as err:
            logger.error(f"Timed out while connecting to server/relay {server}: {err}")
        except Exception as err:
            logger.error(
                f"Exception encountered when trying to connect to server/relay {server}: {err}"
            )

    for server in server_iterator:
        t = create_daemon_thread(
            target=_send_relay_control_message,
            name="SendControlRelayMessageThread",
            args=(server,),
        )
        t.start()


def _send_relay_control_message(server: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d_socket:
        d_socket.settimeout(MEDIUM_REQUEST_TIMEOUT)

        try:
            address, port = address_to_ip_port(server)
            d_socket.connect((address, int(port)))
            d_socket.send(RELAY_CONTROL_MESSAGE)
            logger.info(f"Control message was sent to the server/relay {server}")
        except OSError as err:
            logger.error(f"Error connecting to socket {server}: {err}")
