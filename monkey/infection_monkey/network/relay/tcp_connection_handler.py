import logging
import socket
from threading import Thread
from typing import Callable, List

from monkeytypes import NetworkPort

from infection_monkey.utils.threading import InterruptableThreadMixin

PROXY_TIMEOUT = 2.5

logger = logging.getLogger(__name__)


class TCPConnectionHandler(Thread, InterruptableThreadMixin):
    """Accepts connections on a TCP socket."""

    def __init__(
        self,
        bind_host: str,
        bind_port: NetworkPort,
        client_connected: List[Callable[[socket.socket], None]] = [],
    ):
        self.bind_host = bind_host
        self.bind_port = int(bind_port)
        self._client_connected = client_connected

        Thread.__init__(self, name="TCPConnectionHandler", daemon=True)
        InterruptableThreadMixin.__init__(self)

    def run(self):
        try:
            l_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            l_socket.bind((self.bind_host, self.bind_port))
            l_socket.settimeout(PROXY_TIMEOUT)
            l_socket.listen(5)

            while not self._interrupted.is_set():
                try:
                    source, _ = l_socket.accept()
                except socket.timeout:
                    continue

                logging.debug(f"New connection received from: {source.getpeername()}")
                for notify_client_connected in self._client_connected:
                    notify_client_connected(source)
        except OSError:
            logging.exception("Uncaught error in TCPConnectionHandler thread")
        finally:
            l_socket.close()

        logging.info("Exiting connection handler.")
