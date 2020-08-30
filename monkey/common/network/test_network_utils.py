from unittest import TestCase

from common.network.network_utils import get_host_from_network_location


class TestNetworkUtils(TestCase):
    def test_remove_port_from_ip_string(self):
        assert get_host_from_network_location("127.0.0.1:12345") == "127.0.0.1"
        assert get_host_from_network_location("127.0.0.1:12345") == "127.0.0.1"
        assert get_host_from_network_location("127.0.0.1") == "127.0.0.1"
        assert get_host_from_network_location("www.google.com:8080") == "www.google.com"
        assert get_host_from_network_location("user:password@host:8080") == "host"
