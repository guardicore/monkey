from __future__ import annotations

import select
from logging import getLogger
from threading import Thread
from typing import Callable

READ_BUFFER_SIZE = 8192
SOCKET_READ_TIMEOUT = 10

logger = getLogger(__name__)


class SocketsPipe(Thread):
    def __init__(
        self,
        source,
        dest,
        pipe_closed: Callable[[SocketsPipe], None],
        timeout=SOCKET_READ_TIMEOUT,
    ):
        self.source = source
        self.dest = dest
        self.timeout = timeout
        super().__init__(name=f"SocketsPipeThread-{self.ident}", daemon=True)
        self._pipe_closed = pipe_closed

    def _pipe(self):
        sockets = [self.source, self.dest]
        while True:
            # TODO: Figure out how to capture when the socket times out.
            read_list, _, except_list = select.select(sockets, [], sockets, self.timeout)
            if except_list:
                raise Exception("select() failed")

            if not read_list:
                raise TimeoutError("")

            for r in read_list:
                other = self.dest if r is self.source else self.source
                data = r.recv(READ_BUFFER_SIZE)
                if data:
                    other.sendall(data)

    def run(self):
        try:
            self._pipe()
        except Exception as err:
            logger.debug(err)

        try:
            self.source.close()
        except Exception as err:
            logger.debug(f"Error while closing source socket: {err}")

        try:
            self.dest.close()
        except Exception as err:
            logger.debug(f"Error while closing destination socket: {err}")

        self._pipe_closed(self)
