import socket
from ipaddress import IPv4Address

from .relay_user_handler import RelayUserHandler
from .tcp_pipe_spawner import TCPPipeSpawner

RELAY_CONTROL_MESSAGE = b"infection-monkey-relay-control-message: -"


class RelayConnectionHandler:
    def __init__(self, pipe_spawner: TCPPipeSpawner, relay_user_handler: RelayUserHandler):
        self._pipe_spawner = pipe_spawner
        self._relay_user_handler = relay_user_handler

    def handle_new_connection(self, sock: socket.socket):
        control_message = sock.recv(socket.MSG_PEEK)
        addr, _ = sock.getpeername()  # TODO check the type of the addr object
        if control_message.startswith(RELAY_CONTROL_MESSAGE):
            self._relay_user_handler.disconnect_user(IPv4Address(addr))
        else:
            self._relay_user_handler.add_relay_user(IPv4Address(addr))
            self._pipe_spawner.spawn_pipe(sock)
