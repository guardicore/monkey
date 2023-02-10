import pytest

from common.types import SocketAddress

GOOD_IP = "192.168.1.1"
BAD_IP = "192.168.1.999"
GOOD_PORTS = [0, 1, 1234, 65535]
BAD_PORTS = [99999, 65536, -1]


@pytest.mark.parametrize("good_port", GOOD_PORTS)
def test_socket_address__from_string(good_port):
    expected = SocketAddress(ip=GOOD_IP, port=good_port)

    address = SocketAddress.from_string(f"{GOOD_IP}:{good_port}")

    assert address == expected


@pytest.mark.parametrize(
    "bad_address",
    [
        "not an address",
        ":",
        GOOD_IP,
        f"{GOOD_IP}:",
        "25",
        ":22",
        *[f"{BAD_IP}:{p}" for p in GOOD_PORTS],
        *[f"{GOOD_IP}:{bad_port}" for bad_port in BAD_PORTS],
    ],
)
def test_socket_address__from_string_raises(bad_address: str):
    with pytest.raises(ValueError):
        SocketAddress.from_string(bad_address)
