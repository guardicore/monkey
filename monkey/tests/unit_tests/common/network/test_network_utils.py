from common.network.network_utils import address_to_ip_port


def test_address_to_ip_port():
    ip, port = address_to_ip_port("192.168.65.1:5000")
    assert ip == "192.168.65.1"
    assert port == "5000"


def test_address_to_ip_port_no_port():
    ip, port = address_to_ip_port("192.168.65.1")
    assert port is None

    ip, port = address_to_ip_port("192.168.65.1:")
    assert port is None
