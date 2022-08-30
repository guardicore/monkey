from dataclasses import dataclass
from threading import Event, Lock, Thread
from time import sleep
from typing import List

from infection_monkey.transport.tcp import TcpProxy


@dataclass
class RelayUser:
    address: str


class TCPRelay(Thread):
    """Provides and manages a TCP proxy connection."""

    def __init__(self, local_port: int, target_addr: str, target_port: int):
        self._stopped = Event()
        self._local_port = local_port
        self._target_addr = target_addr
        self._target_port = target_port
        super(TCPRelay, self).__init__(name="MonkeyTcpRelayThread")
        self.daemon = True
        self._relay_users: List[RelayUser] = []
        self._lock = Lock()

    def run(self):
        proxy = TcpProxy(
            local_port=self._local_port,
            dest_host=self._target_addr,
            dest_port=self._target_port,
            client_connected=self.on_user_connected,
            client_disconnected=self.on_user_disconnected,
        )
        proxy.start()

        while not self._stopped.is_set():
            sleep(0.001)

        proxy.stop()
        proxy.join()

    def stop(self):
        self._stopped.set()

    def on_user_connected(self, user: str):
        with self._lock:
            self._relay_users.append(RelayUser(user))

    def on_user_disconnected(self, user: str):
        with self._lock:
            self._relay_users = [u for u in self._relay_users if u.address != user]

    def relay_users(self) -> List[RelayUser]:
        with self._lock:
            return self._relay_users.copy()
