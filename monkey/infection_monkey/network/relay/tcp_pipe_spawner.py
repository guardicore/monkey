import socket
from logging import getLogger
from threading import Lock
from typing import Callable, Set

from monkeytypes import SocketAddress

from .consts import SOCKET_TIMEOUT
from .sockets_pipe import SocketsPipe

logger = getLogger(__name__)


class TCPPipeSpawner:
    """
    Creates bi-directional pipes between the configured client and other clients.
    """

    def __init__(self, target_addr: SocketAddress):
        self._target_ip = target_addr.ip
        self._target_port = target_addr.port
        self._pipes: Set[SocketsPipe] = set()
        self._lock = Lock()

    def spawn_pipe(
        self, source: socket.socket, handle_pipe_data: Callable[[socket.socket, bytes], None]
    ):
        """
        Attempt to create a pipe on between the configured client and the provided socket

        :param source: A socket to the connecting client.
        :raises OSError: If a socket to the configured client could not be created.
        """
        dest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest.settimeout(SOCKET_TIMEOUT)
        try:
            dest.connect((str(self._target_ip), self._target_port))
        except OSError as err:
            source.close()
            dest.close()
            raise err

        pipe = SocketsPipe(
            source,
            dest,
            self._handle_pipe_closed,
            handle_pipe_data,
        )
        with self._lock:
            self._pipes.add(pipe)

        pipe.start()

    def has_open_pipes(self) -> bool:
        """Return whether or not the TCPPipeSpawner has any open pipes."""
        with self._lock:
            for p in self._pipes:
                if p.is_alive():
                    return True

        return False

    def _handle_pipe_closed(self, pipe: SocketsPipe):
        with self._lock:
            logger.debug(f"Closing pipe {pipe}")
            self._pipes.discard(pipe)
