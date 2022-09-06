from dataclasses import dataclass
from ipaddress import IPv4Address
from threading import Lock
from typing import Dict

from egg_timer import EggTimer

from monkey.common.utils.code_utils import del_key

DEFAULT_NEW_CLIENT_TIMEOUT = 3  # Wait up to 3 seconds for potential new clients to connect


@dataclass
class RelayUser:
    address: IPv4Address
    timer: EggTimer


class RelayUserHandler:
    """Manages membership to a network relay."""

    def __init__(self, new_client_timeout: float = DEFAULT_NEW_CLIENT_TIMEOUT):
        self._new_client_timeout = new_client_timeout
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
                del_key(self._potential_users, user_address)

            timer = EggTimer()
            self._relay_users[user_address] = RelayUser(user_address, timer)

    def add_potential_user(self, user_address: IPv4Address):
        """
        Notify RelayUserHandler that a new user may try and connect.

        :param user_address: An address defining potential RelayUser
            that tries to connect to the relay
        """
        with self._lock:
            timer = EggTimer()
            timer.set(self._new_client_timeout)
            self._potential_users[user_address] = RelayUser(user_address, timer)

    def disconnect_user(self, user_address: IPv4Address):
        """
        Handle when a user disconnects.

        :param user_address: The address of the disconnecting user.
        """
        with self._lock:
            if user_address in self._relay_users:
                del_key(self._relay_users, user_address)

    def has_potential_users(self) -> bool:
        """
        Return whether or not we have any potential users.
        """
        self._potential_users = dict(
            filter(lambda ru: not ru[1].timer.is_expired(), self._potential_users.items())
        )

        return len(self._potential_users) > 0
