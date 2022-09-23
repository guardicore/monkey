import pytest

from common.types import SocketAddress
from common.types.utils import socketaddress_from_string

GOOD_IP = "192.168.1.1"
BAD_IP = "192.168.1.999"
GOOD_PORT = 1234
BAD_PORT = 99999


def test_socketaddress_from_string():
    expected = SocketAddress(ip=GOOD_IP, port=GOOD_PORT)

    address = socketaddress_from_string(f"{GOOD_IP}:{GOOD_PORT}")

    assert address == expected


@pytest.mark.parametrize(
    "bad_address",
    [
        "not an address",
        ":",
        GOOD_IP,
        str(GOOD_PORT),
        f"{GOOD_IP}:",
        f":{GOOD_PORT}",
        f"{BAD_IP}:{GOOD_PORT}",
        f"{GOOD_IP}:{BAD_PORT}",
    ],
)
def test_socketaddress_from_string__raises(bad_address: str):
    with pytest.raises(ValueError):
        socketaddress_from_string(bad_address)
