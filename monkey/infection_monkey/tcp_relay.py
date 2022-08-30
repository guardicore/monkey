from threading import Event, Thread
from time import sleep

from infection_monkey.transport.tcp import TcpProxy


class TCPRelay(Thread):
    """Provides and manages a TCP proxy connection."""

    def __init__(self, local_port: int, target_addr: str, target_port: int):
        self._stopped = Event()
        self._local_port = local_port
        self._target_addr = target_addr
        self._target_port = target_port
        super(TCPRelay, self).__init__(name="MonkeyTcpRelayThread")
        self.daemon = True

    def run(self):
        proxy = TcpProxy(
            local_port=self._local_port, dest_host=self._target_addr, dest_port=self._target_port
        )
        proxy.start()

        while not self._stopped.is_set():
            sleep(0.001)

        proxy.stop()
        proxy.join()

    def stop(self):
        self._stopped.set()
