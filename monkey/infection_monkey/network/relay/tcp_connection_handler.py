import socket
from threading import Thread
from typing import Callable, List

from infection_monkey.utils.threading import InterruptableThreadMixin

PROXY_TIMEOUT = 2.5


class TCPConnectionHandler(Thread, InterruptableThreadMixin):
    """Accepts connections on a TCP socket."""

    def __init__(
        self,
        bind_host: str,
        bind_port: int,
        client_connected: List[Callable[[socket.socket], None]] = [],
    ):
        self.bind_host = bind_host
        self.bind_port = bind_port
        self._client_connected = client_connected
        super().__init__(name="TCPConnectionHandler", daemon=True)

    def run(self):
        l_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        l_socket.bind((self.bind_host, self.bind_port))
        l_socket.settimeout(PROXY_TIMEOUT)
        l_socket.listen(5)

        while not self._interrupted.is_set():
            try:
                source, _ = l_socket.accept()
            except socket.timeout:
                continue

            for notify_client_connected in self._client_connected:
                notify_client_connected(source)

        l_socket.close()
