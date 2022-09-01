import socket
from ipaddress import IPv4Address
from threading import Event, Lock, Thread
from time import sleep, time
from typing import List

from infection_monkey.network.relay import (
    RelayUser,
    RelayUserHandler,
    SocketsPipe,
    TCPConnectionHandler,
)

DEFAULT_NEW_CLIENT_TIMEOUT = 3  # Wait up to 3 seconds for potential new clients to connect


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

        self._user_handler = RelayUserHandler()
        self._connection_handler = TCPConnectionHandler(
            local_port, client_connected=self._user_connected
        )
        self._local_port = local_port
        self._target_addr = target_addr
        self._target_port = target_port
        self._new_client_timeout = new_client_timeout
        super().__init__(name="MonkeyTcpRelayThread")
        self.daemon = True
        self._lock = Lock()
        self._pipes: List[SocketsPipe] = []

    def run(self):
        self._connection_handler.start()

        self._stopped.wait()
        self._wait_for_users_to_disconnect()

        self._connection_handler.stop()
        self._connection_handler.join()

        [pipe.join() for pipe in self._pipes]

    def stop(self):
        self._stopped.set()

    def _user_connected(self, source: socket.socket, user_addr: IPv4Address):
        self._user_handler.add_relay_user(user_addr)
        self._spawn_pipe(source)

    def _spawn_pipe(self, source: socket.socket):
        dest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            dest.connect((self._target_addr, self._target_port))
        except socket.error:
            source.close()
            dest.close()

        pipe = SocketsPipe(
            source, dest, client_data_received=self._user_handler.on_user_data_received
        )
        self._pipes.append(pipe)
        pipe.run()

    def _wait_for_users_to_disconnect(self):
        stop = False
        while not stop:
            sleep(0.01)
            current_time = time()
            potential_users = self._user_handler.get_potential_users()
            most_recent_potential_time = max(
                potential_users.values(),
                key=lambda ru: ru.last_update_time,
                default=RelayUser(IPv4Address(""), 0.0),
            ).last_update_time
            potential_elapsed = current_time - most_recent_potential_time

            stop = not potential_users or potential_elapsed > self._new_client_timeout
