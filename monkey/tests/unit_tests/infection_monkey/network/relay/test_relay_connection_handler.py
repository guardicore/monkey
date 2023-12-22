import socket
from ipaddress import IPv4Address
from unittest.mock import MagicMock

import pytest

from infection_monkey.network.relay import (
    RELAY_CONTROL_MESSAGE_REMOVE_FROM_WAITLIST,
    RelayConnectionHandler,
    RelayUserHandler,
    TCPPipeSpawner,
)

USER_ADDRESS = "0.0.0.1"


@pytest.fixture
def pipe_spawner():
    return MagicMock(spec=TCPPipeSpawner)


@pytest.fixture
def relay_user_handler():
    return MagicMock(spec=RelayUserHandler)


@pytest.fixture
def close_socket():
    sock = MagicMock(spec=socket.socket)
    sock.recv.return_value = RELAY_CONTROL_MESSAGE_REMOVE_FROM_WAITLIST
    sock.getpeername.return_value = (USER_ADDRESS, 12345)
    return sock


@pytest.fixture
def data_socket():
    sock = MagicMock(spec=socket.socket)
    sock.recv.return_value = b"some data"
    sock.getpeername.return_value = (USER_ADDRESS, 12345)
    return sock


def test_control_message_disconnects_user(pipe_spawner, relay_user_handler, close_socket):
    connection_handler = RelayConnectionHandler(pipe_spawner, relay_user_handler)

    connection_handler.handle_new_connection(close_socket)

    relay_user_handler.disconnect_user.assert_called_once_with(IPv4Address(USER_ADDRESS))


def test_connection_spawns_pipe(pipe_spawner, relay_user_handler, data_socket):
    connection_handler = RelayConnectionHandler(pipe_spawner, relay_user_handler)

    connection_handler.handle_new_connection(data_socket)

    pipe_spawner.spawn_pipe.assert_called_once()
    assert pipe_spawner.spawn_pipe.call_args[0][0] == data_socket


def test_connection_adds_user(pipe_spawner, relay_user_handler, data_socket):
    connection_handler = RelayConnectionHandler(pipe_spawner, relay_user_handler)

    connection_handler.handle_new_connection(data_socket)

    relay_user_handler.add_relay_user.assert_called_once_with(IPv4Address(USER_ADDRESS))
