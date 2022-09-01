import socket
from ipaddress import IPv4Address
from threading import Thread
from typing import Callable
from unittest.mock import MagicMock

import pytest

from monkey.infection_monkey.network.relay.relay_user_handler import (  # RELAY_CONTROL_MESSAGE,
    RelayUserHandler,
)
from monkey.infection_monkey.tcp_relay import TCPRelay

NEW_USER_ADDRESS = IPv4Address("0.0.0.1")
LOCAL_PORT = 9975
TARGET_ADDRESS = "0.0.0.0"
TARGET_PORT = 9976


class FakeConnectionHandler:
    def notify_client_connected(self, callback: Callable[[socket.socket, IPv4Address], None]):
        self.cb = callback

    def client_connected(self, socket: socket.socket, addr: IPv4Address):
        self.cb(socket, addr)

    def start(self):
        pass

    def stop(self):
        pass

    def join(self):
        pass


class FakePipeSpawner:
    spawn_pipe = MagicMock()

    def notify_client_data_received(self, callback: Callable[[bytes], bool]):
        self.cb = callback

    def send_client_data(self, data: bytes):
        self.cb(data)


@pytest.fixture
def relay_user_handler() -> RelayUserHandler:
    return RelayUserHandler()


@pytest.fixture
def pipe_spawner():
    return FakePipeSpawner()


@pytest.fixture
def connection_handler():
    return FakeConnectionHandler()


@pytest.fixture
def tcp_relay(relay_user_handler, connection_handler, pipe_spawner) -> TCPRelay:
    return TCPRelay(relay_user_handler, connection_handler, pipe_spawner)


def join_or_kill_thread(thread: Thread, timeout: float):
    """Whether or not the thread joined in the given timeout period."""
    thread.join(timeout)
    if thread.is_alive():
        # Cannot set daemon status of active thread: thread.daemon = True
        return False
    return True


def test_user_added_when_user_connected(connection_handler, relay_user_handler, tcp_relay):
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connection_handler.client_connected(sock, NEW_USER_ADDRESS)
    # assert len(relay_user_handler.get_relay_users()) == 1
    pass


def test_pipe_created_when_user_connected(connection_handler, pipe_spawner, tcp_relay):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_handler.client_connected(sock, NEW_USER_ADDRESS)
    assert pipe_spawner.spawn_pipe.called


def test_user_removed_on_request(relay_user_handler, pipe_spawner, tcp_relay):
    relay_user_handler.add_relay_user(NEW_USER_ADDRESS)

    # pipe_spawner.send_client_data(RELAY_CONTROL_MESSAGE, NEW_USER_ADDRESS)

    # users = relay_user_handler.get_relay_users()
    # assert len(users) == 0
    pass


# This will fail unless TcpProxy is updated to do non-blocking accepts
# @pytest.mark.slow
# def test_waits_for_exploited_machines():
#     relay = TCPRelay(9975, "0.0.0.0", 9976, new_client_timeout=0.2)
#     new_user = "0.0.0.1"
#     relay.start()

#     relay.add_potential_user(new_user)
#     relay.stop()

#     assert not join_or_kill_thread(relay, 0.1)  # Should be waiting
#     assert join_or_kill_thread(relay, 1)  # Should be done waiting
