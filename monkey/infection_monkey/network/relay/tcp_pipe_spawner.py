import socket
from ipaddress import IPv4Address
from typing import Callable

from .tcp import SocketsPipe


class TCPPipeSpawner:
    def __init__(self, target_addr: IPv4Address, target_port: int):
        self._target_addr = target_addr
        self._target_port = target_port

    def spawn_pipe(self, source: socket.socket) -> SocketsPipe:
        dest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            dest.connect((self._target_addr, self._target_port))
        except socket.error as err:
            source.close()
            dest.close()
            raise err

        return SocketsPipe(source, dest, client_data_received=self._client_data_received)

    def notify_client_data_received(self, callback: Callable[[bytes], bool]):
        self._client_data_received = callback
