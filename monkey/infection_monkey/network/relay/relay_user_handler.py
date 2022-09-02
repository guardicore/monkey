from dataclasses import dataclass
from ipaddress import IPv4Address
from threading import Lock
from time import time
from typing import Dict

RELAY_CONTROL_MESSAGE = b"infection-monkey-relay-control-message: -"


@dataclass
class RelayUser:
    address: IPv4Address
    last_update_time: float


class RelayUserHandler:
    def __init__(self):
        self._relay_users: Dict[IPv4Address, RelayUser] = {}
        self._potential_users: Dict[IPv4Address, RelayUser] = {}

        self._lock = Lock()

    def add_relay_user(self, user_address: IPv4Address):
        """
        Handle new user connection.

        :param source_socket: A source socket
        :param user_address: An address defining RelayUser which will be added to the relay
        """

        with self._lock:
            if user_address in self._potential_users:
                del self._potential_users[user_address]

            self._relay_users[user_address] = RelayUser(user_address, time())

    def add_potential_user(self, user_address: IPv4Address):
        """
        Notify TCPRelay that a new user may try and connect

        :param user_address: An address defining potential RelayUser
            that tries to connect to the relay
        """
        with self._lock:
            self._potential_users[user_address] = RelayUser(user_address, time())

    def on_user_data_received(self, data: bytes, user_address: IPv4Address) -> bool:
        """
        Disconnect a user with a specific starting data.

        :param data: The data that a relay received
        :param user_address: An address defining RelayUser which received the data
        """
        if data.startswith(RELAY_CONTROL_MESSAGE):
            self.disconnect_user(user_address)
            return False
        return True

    def disconnect_user(self, user_address: IPv4Address):
        """
        Handle when a user disconnects.

        :param user_address: The address of the disconnecting user.
        """
        with self._lock:
            if user_address in self._relay_users:
                del self._relay_users[user_address]

    def get_potential_users(self) -> Dict[IPv4Address, RelayUser]:
        with self._lock:
            return self._potential_users.copy()
