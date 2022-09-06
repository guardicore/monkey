import select
from logging import getLogger
from threading import Thread
from typing import Callable

from infection_monkey.transport.base import update_last_serve_time

READ_BUFFER_SIZE = 8192
SOCKET_READ_TIMEOUT = 10

logger = getLogger(__name__)


class SocketsPipe(Thread):
    def __init__(
        self,
        source,
        dest,
        timeout=SOCKET_READ_TIMEOUT,
        client_disconnected: Callable[[str], None] = None,
    ):
        self.source = source
        self.dest = dest
        self.timeout = timeout
        self._keep_connection = True
        super().__init__(name=f"SocketsPipeThread-{self.ident}")
        self.daemon = True
        self._client_disconnected = client_disconnected

    def run(self):
        sockets = [self.source, self.dest]
        while self._keep_connection:
            self._keep_connection = False
            rlist, _, xlist = select.select(sockets, [], sockets, self.timeout)
            if xlist:
                break
            for r in rlist:
                other = self.dest if r is self.source else self.source
                try:
                    data = r.recv(READ_BUFFER_SIZE)
                except Exception:
                    break
                if data:
                    try:
                        other.sendall(data)
                        update_last_serve_time()
                    except Exception:
                        break
                    self._keep_connection = True

        self.source.close()
        self.dest.close()
        if self._client_disconnected:
            self._client_disconnected()
