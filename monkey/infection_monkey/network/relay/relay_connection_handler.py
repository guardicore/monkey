import socket
from ipaddress import IPv4Address

from .relay_user_handler import RelayUserHandler
from .tcp_pipe_spawner import TCPPipeSpawner

RELAY_CONTROL_MESSAGE_REMOVE_FROM_WAITLIST = b"infection-monkey-relay-control-message: -"


class RelayConnectionHandler:
    """Handles new relay connections."""

    def __init__(self, pipe_spawner: TCPPipeSpawner, relay_user_handler: RelayUserHandler):
        self._pipe_spawner = pipe_spawner
        self._relay_user_handler = relay_user_handler

    def handle_new_connection(self, sock: socket.socket):
        """
        Spawn a new pipe, or remove the user if the user requested to disconnect.

        :param sock: The socket for the new connection.
        """
        addr, _ = sock.getpeername()
        addr = IPv4Address(addr)

        control_message = sock.recv(socket.MSG_PEEK)

        if control_message.startswith(RELAY_CONTROL_MESSAGE_REMOVE_FROM_WAITLIST):
            self._relay_user_handler.disconnect_user(addr)
        else:
            self._relay_user_handler.add_relay_user(addr)
            self._pipe_spawner.spawn_pipe(sock)
