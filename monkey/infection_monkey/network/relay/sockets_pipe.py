from __future__ import annotations

import select
import socket
from logging import getLogger
from threading import Thread
from typing import Callable

from .consts import SOCKET_TIMEOUT

READ_BUFFER_SIZE = 8192

logger = getLogger(__name__)


class SocketsPipe(Thread):
    """Manages a pipe between two sockets."""

    _thread_count: int = 0

    def __init__(
        self,
        source,
        dest,
        on_pipe_closed: Callable[[SocketsPipe], None],
        on_pipe_received_data: Callable[[socket.socket, bytes], None],
        timeout=SOCKET_TIMEOUT,
    ):
        self.source = source
        self.dest = dest
        self.timeout = timeout
        super().__init__(name=f"SocketsPipeThread-{self._next_thread_num()}", daemon=True)
        self._on_pipe_closed = on_pipe_closed
        self._on_pipe_received_data = on_pipe_received_data

    @classmethod
    def _next_thread_num(cls):
        cls._thread_count += 1
        return cls._thread_count

    def _pipe(self):
        sockets = [self.source, self.dest]
        socket_closed = False

        while not socket_closed:
            read_list, _, except_list = select.select(sockets, [], sockets, self.timeout)
            if except_list:
                raise OSError(f"select() failed on sockets {except_list}")

            if not read_list:
                raise TimeoutError(f"pipe did not receive data for {self.timeout} seconds")

            for r in read_list:
                other = self.dest if r is self.source else self.source
                data = r.recv(READ_BUFFER_SIZE)
                if data:
                    other.sendall(data)
                    self._on_pipe_received_data(r, data)
                else:
                    socket_closed = True
                    break

    def run(self):
        try:
            self._pipe()
        except OSError as err:
            logger.debug(err)

        try:
            self.source.close()
        except OSError as err:
            logger.debug(f"Error while closing source socket: {err}")

        try:
            self.dest.close()
        except OSError as err:
            logger.debug(f"Error while closing destination socket: {err}")

        self._on_pipe_closed(self)
