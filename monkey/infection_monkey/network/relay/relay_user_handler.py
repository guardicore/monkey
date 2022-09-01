import socket
from dataclasses import dataclass
from ipaddress import IPv4Address
from time import time
from typing import Callable, Dict

from threding import Lock

RELAY_CONTROL_MESSAGE = b"infection-monkey-relay-control-message: -"


@dataclass
class RelayUser:
    address: IPv4Address
    last_update_time: float


class RelayUserHandler:
    def __init__(self, spawn_new_pipe: Callable[[socket.socket, IPv4Address], None]):
        self._relay_users: Dict[IPv4Address, RelayUser] = {}
        self._potential_users: Dict[IPv4Address, RelayUser] = {}
        self._spawn_new_pipe = spawn_new_pipe

        self._lock = Lock()

    def add_relay_user(self, source_socket: socket.socket, user_address: IPv4Address):
        """
        Handle new user connection.

        :param source_socket: A source socket
        :param user_addres: An address defining RelayUser which will be added to the relay
        """

        with self._lock:
            if user_address in self._potential_users:
                del self._potential_users[user_address]

            self._relay_users[user_address] = RelayUser(user_address, time())
            self._spawn_new_pipe(source_socket, user_address)

    def add_potential_user(self, user_address: IPv4Address):
        """
        Notify TCPRelay that a new user may try and connect

        :param user_address: An address defining potential RelayUser
            that tries to connect to the relay
        """
        with self._lock:
            self._potential_users[user_address] = RelayUser(user_address, time())

    def on_user_data_recieved(self, data: bytes, user_address: IPv4Address) -> bool:
        """
        Disconnect a user with a specific starting data.

        :param data: The data that a relay recieved
        :param user_address: An address defining RelayUser which recieved the data
        """
        if data.startswith(RELAY_CONTROL_MESSAGE):
            self._disconnect_user(user_address)
            return False
        return True

    def _disconnect_user(self, user_address: IPv4Address):
        with self._lock:
            if user_address in self._relay_users:
                del self._relay_users[user_address]
