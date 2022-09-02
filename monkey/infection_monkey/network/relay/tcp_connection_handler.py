import socket
from threading import Event, Thread
from typing import Callable, List

PROXY_TIMEOUT = 2.5


class TCPConnectionHandler(Thread):
    """Accepts connections on a TCP socket."""

    def __init__(
        self,
        local_port: int,
        local_host: str = "",
        client_connected: List[Callable[[socket.socket], None]] = [],
    ):
        self.local_port = local_port
        self.local_host = local_host
        self._client_connected = client_connected
        super().__init__(name="TCPConnectionHandler", daemon=True)
        self._stopped = Event()

    def run(self):
        l_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        l_socket.bind((self.local_host, self.local_port))
        l_socket.settimeout(PROXY_TIMEOUT)
        l_socket.listen(5)

        while not self._stopped:
            try:
                source, _ = l_socket.accept()
            except socket.timeout:
                continue

            for notify_client_connected in self._client_connected:
                notify_client_connected(source)

        l_socket.close()

    def stop(self):
        self._stopped.set()
