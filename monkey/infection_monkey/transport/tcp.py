import select
import socket
from functools import partial
from logging import getLogger
from threading import Thread
from typing import Callable

from infection_monkey.transport.base import (
    PROXY_TIMEOUT,
    TransportProxyBase,
    update_last_serve_time,
)

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
        Thread.__init__(self)
        self.source = source
        self.dest = dest
        self.timeout = timeout
        self._keep_connection = True
        super(SocketsPipe, self).__init__()
        self.daemon = True
        self._client_disconnected = client_disconnected

    def run(self):
        sockets = [self.source, self.dest]
        while self._keep_connection:
            self._keep_connection = False
            rlist, wlist, xlist = select.select(sockets, [], sockets, self.timeout)
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


class TcpProxy(TransportProxyBase):
    def __init__(
        self,
        local_port,
        dest_host=None,
        dest_port=None,
        local_host="",
        client_connected: Callable[[str], None] = None,
        client_disconnected: Callable[[str], None] = None,
    ):
        super().__init__(local_port, dest_host, dest_port, local_host)
        self._client_connected = client_connected
        self._client_disconnected = client_disconnected

    def run(self):
        pipes = []
        l_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        l_socket.bind((self.local_host, self.local_port))
        l_socket.settimeout(PROXY_TIMEOUT)
        l_socket.listen(5)

        while not self._stopped:
            try:
                source, address = l_socket.accept()
            except socket.timeout:
                continue

            dest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                dest.connect((self.dest_host, self.dest_port))
            except socket.error:
                source.close()
                dest.close()
                continue

            on_disconnect = (
                partial(self._client_connected, address[0]) if self._client_connected else None
            )
            pipe = SocketsPipe(source, dest, on_disconnect)
            pipes.append(pipe)
            logger.debug(
                "piping sockets %s:%s->%s:%s",
                address[0],
                address[1],
                self.dest_host,
                self.dest_port,
            )
            if self._client_connected:
                self._client_connected(address[0])
            pipe.start()

        l_socket.close()
        for pipe in pipes:
            pipe.join()
