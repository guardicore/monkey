from ipaddress import IPv4Address
from threading import Lock, Thread
from time import sleep

from infection_monkey.network.relay import (
    RelayConnectionHandler,
    RelayUserHandler,
    TCPConnectionHandler,
    TCPPipeSpawner,
)
from infection_monkey.utils.threading import InterruptableThreadMixin


class TCPRelay(Thread, InterruptableThreadMixin):
    """
    Provides and manages a TCP proxy connection.
    """

    def __init__(
        self,
        relay_port: int,
        dest_addr: IPv4Address,
        dest_port: int,
        client_disconnect_timeout: float,
    ):
        self._user_handler = RelayUserHandler(client_disconnect_timeout=client_disconnect_timeout)
        self._pipe_spawner = TCPPipeSpawner(dest_addr, dest_port)
        relay_filter = RelayConnectionHandler(self._pipe_spawner, self._user_handler)
        self._connection_handler = TCPConnectionHandler(
            bind_host="",
            bind_port=relay_port,
            client_connected=[
                relay_filter.handle_new_connection,
            ],
        )
        super().__init__(name="MonkeyTcpRelayThread", daemon=True)
        self._lock = Lock()

    def run(self):
        self._connection_handler.start()

        self._interrupted.wait()
        self._wait_for_users_to_disconnect()

        self._connection_handler.stop()
        self._connection_handler.join()
        self._wait_for_pipes_to_close()

    def add_potential_user(self, user_address: IPv4Address):
        """
        Notify TCPRelay of a user that may try to connect.

        :param user_address: The address of the potential new user.
        """
        self._user_handler.add_potential_user(user_address)

    def _wait_for_users_to_disconnect(self):
        """
        Blocks until the users disconnect or the timeout has elapsed.
        """
        while self._user_handler.has_potential_users() or self._user_handler.has_connected_users():
            sleep(0.5)

    def _wait_for_pipes_to_close(self):
        """
        Blocks until the pipes have closed.
        """
        while self._pipe_spawner.has_open_pipes():
            sleep(0.5)
