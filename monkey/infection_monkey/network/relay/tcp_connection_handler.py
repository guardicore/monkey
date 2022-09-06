import socket
from threading import Event, Thread
from typing import Callable, List

PROXY_TIMEOUT = 2.5


class TCPConnectionHandler(Thread):
    """Accepts connections on a TCP socket."""

    def __init__(
        self,
        bind_host: str,
        bind_port: int,
        client_connected: List[Callable[[socket.socket], None]] = [],
    ):
        self.local_port = bind_port
        self.local_host = bind_host
        self._client_connected = client_connected
        super().__init__(name="TCPConnectionHandler", daemon=True)
        self._stopped = Event()

    def run(self):
        l_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        l_socket.bind((self.bind_host, self.bind_port))
        l_socket.settimeout(PROXY_TIMEOUT)
        l_socket.listen(5)

        while not self._stopped.is_set():
            try:
                source, _ = l_socket.accept()
            except socket.timeout:
                continue

            for notify_client_connected in self._client_connected:
                notify_client_connected(source)

        l_socket.close()

    def stop(self):
        self._stopped.set()
