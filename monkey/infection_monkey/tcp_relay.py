from dataclasses import dataclass
from ipaddress import IPv4Address
from threading import Event, Lock, Thread
from time import sleep, time
from typing import Dict

from infection_monkey.transport.tcp import TcpProxy

DEFAULT_NEW_CLIENT_TIMEOUT = 3  # Wait up to 3 seconds for potential new clients to connect
RELAY_CONTROL_MESSAGE = b"infection-monkey-relay-control-message: -"


@dataclass
class RelayUser:
    address: IPv4Address
    last_update_time: float


class TCPRelay(Thread):
    """
    Provides and manages a TCP proxy connection.
    """

    def __init__(
        self,
        local_port: int,
        target_addr: str,
        target_port: int,
        new_client_timeout: float = DEFAULT_NEW_CLIENT_TIMEOUT,
    ):
        self._stopped = Event()
        self._local_port = local_port
        self._target_addr = target_addr
        self._target_port = target_port
        self._new_client_timeout = new_client_timeout
        super(TCPRelay, self).__init__(name="MonkeyTcpRelayThread")
        self.daemon = True
        self._relay_users: Dict[IPv4Address, RelayUser] = {}
        self._potential_users: Dict[IPv4Address, RelayUser] = {}
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

        self._stopped.wait()

        self._wait_for_users_to_disconnect()

        proxy.stop()
        proxy.join()

    def stop(self):
        self._stopped.set()

    def on_user_connected(self, user_address: IPv4Address):
        """
        Handle new user connection.

        :param user: A user which will be added to the relay
        """
        with self._lock:
            if user_address in self._potential_users:
                del self._potential_users[user_address]

            self._relay_users[user_address] = RelayUser(user_address, time())

    def on_user_disconnected(self, user_address: IPv4Address):
        """Handle user disconnection."""
        pass

    def relay_users(self) -> Dict[IPv4Address, RelayUser]:
        """
        Get the list of users connected to the relay.
        """
        with self._lock:
            return self._relay_users.copy()

    def on_potential_new_user(self, user_address: IPv4Address):
        """
        Notify TCPRelay that a new user may try and connect.

        :param user: A potential user that tries to connect to the relay
        """
        with self._lock:
            self._potential_users[user_address] = RelayUser(user_address, time())

    def on_user_data_received(self, data: bytes, user_address: IPv4Address) -> bool:
        """
        Disconnect a user which a specific starting data.

        :param data: The data that a relay recieved
        :param user: User which send the data
        """
        if data.startswith(RELAY_CONTROL_MESSAGE):
            self._disconnect_user(user_address)
            return False
        return True

    def _disconnect_user(self, user_address: IPv4Address):
        with self._lock:
            if user_address in self._relay_users:
                del self._relay_users[user_address]

    def _wait_for_users_to_disconnect(self):
        stop = False
        while not stop:
            sleep(0.01)
            current_time = time()
            most_recent_potential_time = max(
                self._potential_users.values(),
                key=lambda ru: ru.last_update_time,
                default=RelayUser(IPv4Address(""), 0.0),
            ).last_update_time
            potential_elapsed = current_time - most_recent_potential_time

            stop = not self._potential_users or potential_elapsed > self._new_client_timeout
