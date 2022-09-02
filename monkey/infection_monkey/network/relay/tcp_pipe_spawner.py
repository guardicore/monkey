import socket
from ipaddress import IPv4Address
from typing import List

from .tcp import SocketsPipe


class TCPPipeSpawner:
    """
    Creates bi-directional pipes between the configured client and other clients.
    """

    def __init__(self, target_addr: IPv4Address, target_port: int):
        self._target_addr = target_addr
        self._target_port = target_port
        self._pipes: List[SocketsPipe] = []

    def spawn_pipe(self, source: socket.socket):
        dest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            dest.connect((self._target_addr, self._target_port))
        except socket.error as err:
            source.close()
            dest.close()
            raise err

        # TODO: have SocketsPipe notify TCPPipeSpawner when it's done
        pipe = SocketsPipe(source, dest)
        self._pipes.append(pipe)
        pipe.run()

    def has_open_pipes(self) -> bool:
        self._pipes = [p for p in self._pipes if p.is_alive()]
        return len(self._pipes) > 0
