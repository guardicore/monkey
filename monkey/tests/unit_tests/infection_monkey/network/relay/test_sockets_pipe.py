from unittest.mock import MagicMock

from infection_monkey.network.relay import SocketsPipe


def test_sockets_pipe__name_increments():
    sock_in = MagicMock()
    sock_out = MagicMock()

    pipe1 = SocketsPipe(sock_in, sock_out, None)
    assert pipe1.name.endswith("1")

    pipe2 = SocketsPipe(sock_in, sock_out, None)
    assert pipe2.name.endswith("2")
