from ipaddress import IPv4Address
from logging import getLogger
from threading import Lock, Thread
from time import sleep

from monkeytypes import NetworkPort, SocketAddress

from infection_monkey.network.relay import (
    RelayConnectionHandler,
    RelayUserHandler,
    TCPConnectionHandler,
    TCPPipeSpawner,
)
from infection_monkey.utils.threading import InterruptableThreadMixin

logger = getLogger(__name__)


class TCPRelay(Thread, InterruptableThreadMixin):
    """
    Provides and manages a TCP proxy connection.
    """

    def __init__(
        self,
        relay_port: NetworkPort,
        dest_address: SocketAddress,
        client_disconnect_timeout: float,
    ):
        self._user_handler = RelayUserHandler(
            new_client_timeout=client_disconnect_timeout,
            client_disconnect_timeout=client_disconnect_timeout,
        )
        self._pipe_spawner = TCPPipeSpawner(dest_address)
        relay_filter = RelayConnectionHandler(self._pipe_spawner, self._user_handler)
        self._connection_handler = TCPConnectionHandler(
            bind_host="",
            bind_port=relay_port,
            client_connected_listeners=[
                relay_filter.handle_new_connection,
            ],
        )
        super().__init__(name="MonkeyTcpRelayThread", daemon=True)
        InterruptableThreadMixin.__init__(self)
        self._lock = Lock()

    def run(self):
        self._connection_handler.start()

        self._interrupted.wait()
        self._wait_for_users_to_disconnect()

        self._connection_handler.stop()
        self._connection_handler.join()
        self._wait_for_pipes_to_close()
        logger.info("TCP Relay closed.")

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
