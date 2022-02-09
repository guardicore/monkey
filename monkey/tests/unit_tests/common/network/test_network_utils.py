from unittest import TestCase

from common.network.network_utils import address_to_ip_port, remove_port


class TestNetworkUtils(TestCase):
    def test_remove_port_from_url(self):
        assert remove_port("https://google.com:80") == "https://google.com"
        assert remove_port("https://8.8.8.8:65336") == "https://8.8.8.8"
        assert remove_port("ftp://ftpserver.com:21/hello/world") == "ftp://ftpserver.com"


def test_address_to_ip_port():
    ip, port = address_to_ip_port("192.168.65.1:5000")
    assert ip == "192.168.65.1"
    assert port == "5000"


def test_address_to_ip_port_no_port():
    ip, port = address_to_ip_port("192.168.65.1")
    assert port is None

    ip, port = address_to_ip_port("192.168.65.1:")
    assert port is None
