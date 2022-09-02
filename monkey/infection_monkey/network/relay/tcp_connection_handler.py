import socket
from ipaddress import IPv4Address
from threading import Event, Thread
from typing import Callable

PROXY_TIMEOUT = 2.5


class TCPConnectionHandler(Thread):
    """Accepts connections on a TCP socket."""

    def __init__(
        self,
        local_port: int,
        local_host: str = "",
        client_connected: Callable[[socket.socket, IPv4Address], None] = None,
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
                source, address = l_socket.accept()
            except socket.timeout:
                continue

            if self._client_connected:
                self._client_connected(source, IPv4Address(address[0]))

        l_socket.close()

    def stop(self):
        self._stopped.set()

    def notify_client_connected(self, callback: Callable[[socket.socket, IPv4Address], None]):
        """
        Register to be notified when a client connects.

        :param callback: Callable used to notify when a client connects.
        """
        self._client_connected = callback
