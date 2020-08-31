from unittest import TestCase

from monkey_island.cc.resources.bootloader import Bootloader


class TestBootloader(TestCase):

    def test_get_request_contents_linux(self):
        data_without_tunnel = b'{"system":"linux", ' \
                              b'"os_version":"NAME="Ubuntu"\n", ' \
                              b'"glibc_version":"ldd (Ubuntu GLIBC 2.23-0ubuntu11) 2.23\n", ' \
                              b'"hostname":"test-TEST", ' \
                              b'"tunnel":false, ' \
                              b'"ips": ["127.0.0.1", "10.0.2.15", "192.168.56.5"]}'
        data_with_tunnel = b'{"system":"linux", ' \
                           b'"os_version":"NAME="Ubuntu"\n", ' \
                           b'"glibc_version":"ldd (Ubuntu GLIBC 2.23-0ubuntu11) 2.23\n", ' \
                           b'"hostname":"test-TEST", ' \
                           b'"tunnel":"192.168.56.1:5002", ' \
                           b'"ips": ["127.0.0.1", "10.0.2.15", "192.168.56.5"]}'

        result1 = Bootloader._get_request_contents_linux(data_without_tunnel)
        self.assertTrue(result1['system'] == "linux")
        self.assertTrue(result1['os_version'] == "Ubuntu")
        self.assertTrue(result1['glibc_version'] == "ldd (Ubuntu GLIBC 2.23-0ubuntu11) 2.23")
        self.assertTrue(result1['hostname'] == "test-TEST")
        self.assertFalse(result1['tunnel'])
        self.assertTrue(result1['ips'] == ["127.0.0.1", "10.0.2.15", "192.168.56.5"])

        result2 = Bootloader._get_request_contents_linux(data_with_tunnel)
        self.assertTrue(result2['system'] == "linux")
        self.assertTrue(result2['os_version'] == "Ubuntu")
        self.assertTrue(result2['glibc_version'] == "ldd (Ubuntu GLIBC 2.23-0ubuntu11) 2.23")
        self.assertTrue(result2['hostname'] == "test-TEST")
        self.assertTrue(result2['tunnel'] == "192.168.56.1:5002")
        self.assertTrue(result2['ips'] == ["127.0.0.1", "10.0.2.15", "192.168.56.5"])

    def test_get_request_contents_windows(self):
        windows_data = b'{\x00"\x00s\x00y\x00s\x00t\x00e\x00m\x00"\x00:\x00"\x00w\x00i\x00n\x00d\x00o' \
                       b'\x00w\x00s\x00"\x00,\x00 \x00"\x00o\x00s\x00_\x00v\x00e\x00r\x00s\x00i\x00o\x00n' \
                       b'\x00"\x00:\x00"\x00w\x00i\x00n\x00d\x00o\x00w\x00s\x008\x00_\x00o\x00r\x00_\x00g\x00r' \
                       b'\x00e\x00a\x00t\x00e\x00r\x00"\x00,\x00 \x00"\x00h\x00o\x00s\x00t\x00n\x00a\x00m\x00e\x00"' \
                       b'\x00:\x00"\x00D\x00E\x00S\x00K\x00T\x00O\x00P\x00-\x00P\x00J\x00H\x00U\x003\x006\x00B\x00"' \
                       b'\x00,\x00 \x00"\x00t\x00u\x00n\x00n\x00e\x00l\x00"\x00:\x00f\x00a\x00l\x00s\x00e\x00,\x00 ' \
                       b'\x00"\x00i\x00p\x00s\x00"\x00:\x00 \x00[\x00"\x001\x009\x002\x00.\x001\x006\x008\x00.\x005' \
                       b'\x006\x00.\x001\x00"\x00,\x00 \x00"\x001\x009\x002\x00.\x001\x006\x008\x00.\x002\x004\x009' \
                       b'\x00.\x001\x00"\x00,\x00 \x00"\x001\x009\x002\x00.\x001\x006\x008\x00.\x002\x001\x007\x00.' \
                       b'\x001\x00"\x00]\x00}\x00'

        result = Bootloader._get_request_contents_windows(windows_data)
        self.assertTrue(result['system'] == "windows")
        self.assertTrue(result['os_version'] == "windows8_or_greater")
        self.assertTrue(result['hostname'] == "DESKTOP-PJHU36B")
        self.assertFalse(result['tunnel'])
        self.assertTrue(result['ips'] == ["192.168.56.1", "192.168.249.1", "192.168.217.1"])
