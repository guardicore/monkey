from threading import Lock, Thread
from time import sleep

from infection_monkey.network.relay import RelayUserHandler, TCPConnectionHandler, TCPPipeSpawner
from infection_monkey.utils.threading import InterruptableThreadMixin


class TCPRelay(Thread, InterruptableThreadMixin):
    """
    Provides and manages a TCP proxy connection.
    """

    def __init__(
        self,
        relay_user_handler: RelayUserHandler,
        connection_handler: TCPConnectionHandler,
        pipe_spawner: TCPPipeSpawner,
    ):
        self._user_handler = relay_user_handler
        self._connection_handler = connection_handler
        self._pipe_spawner = pipe_spawner
        super().__init__(name="MonkeyTcpRelayThread", daemon=True)
        self._lock = Lock()

    def run(self):
        self._connection_handler.start()

        self._interrupted.wait()
        self._wait_for_users_to_disconnect()

        self._connection_handler.stop()
        self._connection_handler.join()
        self._wait_for_pipes_to_close()

    def _wait_for_users_to_disconnect(self):
        """
        Blocks until the users disconnect or the timeout has elapsed.
        """
        while self._user_handler.has_potential_users():
            sleep(0.5)

    def _wait_for_pipes_to_close(self):
        """
        Blocks until the pipes have closed.
        """
        while self._pipe_spawner.has_open_pipes():
            sleep(0.5)
