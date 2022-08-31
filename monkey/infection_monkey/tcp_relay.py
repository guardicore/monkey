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
        self._potential_users: List[RelayUser] = []
        self._lock = Lock()

    def run(self):
        proxy = TcpProxy(
            local_port=self._local_port,
            dest_host=self._target_addr,
            dest_port=self._target_port,
            client_connected=self.on_user_connected,
            client_disconnected=self.on_user_disconnected,
            client_data_received=self.on_user_data_received,
        )
        proxy.start()

        while not self._stopped.is_set():
            sleep(0.001)

        proxy.stop()
        proxy.join()

    def stop(self):
        self._stopped.set()

    def on_user_connected(self, user: str):
        """Handle new user connection."""
        with self._lock:
            self._potential_users = [u for u in self._potential_users if u.address != user]
            self._relay_users.append(RelayUser(user))

    def on_user_disconnected(self, user: str):
        """Handle user disconnection."""
        pass

    def relay_users(self) -> List[RelayUser]:
        """Get the list of users connected to the relay."""
        with self._lock:
            return self._relay_users.copy()

    def on_potential_new_user(self, user: str):
        """Notify TCPRelay that a new user may try and connect."""
        with self._lock:
            self._potential_users.append(RelayUser(user))

    def on_user_data_received(self, data: bytes, user: str) -> bool:
        if data.startswith(b"-"):
            self._disconnect_user(user)
            return False
        return True

    def _disconnect_user(self, user: str):
        with self._lock:
            self._relay_users = [u for u in self._relay_users if u.address != user]
