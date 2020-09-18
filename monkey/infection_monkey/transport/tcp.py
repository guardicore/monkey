import select
import socket
from logging import getLogger
from threading import Thread

from infection_monkey.transport.base import (TransportProxyBase,
                                             update_last_serve_time)

READ_BUFFER_SIZE = 8192
DEFAULT_TIMEOUT = 30

LOG = getLogger(__name__)


class SocketsPipe(Thread):
    def __init__(self, source, dest, timeout=DEFAULT_TIMEOUT):
        Thread.__init__(self)
        self.source = source
        self.dest = dest
        self.timeout = timeout
        self._keep_connection = True
        super(SocketsPipe, self).__init__()
        self.daemon = True

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
                except:
                    break
                if data:
                    try:
                        other.sendall(data)
                        update_last_serve_time()
                    except:
                        break
                    self._keep_connection = True

        self.source.close()
        self.dest.close()


class TcpProxy(TransportProxyBase):

    def run(self):
        pipes = []
        l_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        l_socket.bind((self.local_host, self.local_port))
        l_socket.settimeout(DEFAULT_TIMEOUT)
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

            pipe = SocketsPipe(source, dest)
            pipes.append(pipe)
            LOG.debug("piping sockets %s:%s->%s:%s", address[0], address[1], self.dest_host, self.dest_port)
            pipe.start()

        l_socket.close()
        for pipe in pipes:
            pipe.join()
