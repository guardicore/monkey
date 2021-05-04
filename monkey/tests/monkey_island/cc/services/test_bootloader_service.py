from unittest import TestCase

from monkey_island.cc.services.bootloader import BootloaderService

MIN_GLIBC_VERSION = 2.14


class TestBootloaderService(TestCase):
    def test_is_glibc_supported(self):
        str1 = "ldd (Ubuntu EGLIBC 2.15-0ubuntu10) 2.15"
        str2 = "ldd (GNU libc) 2.12"
        str3 = "ldd (GNU libc) 2.28"
        str4 = "ldd (Ubuntu GLIBC 2.23-0ubuntu11) 2.23"
        self.assertTrue(
            not BootloaderService.is_glibc_supported(str1)
            and not BootloaderService.is_glibc_supported(str2)
            and BootloaderService.is_glibc_supported(str3)
            and BootloaderService.is_glibc_supported(str4)
        )

    def test_remove_local_ips(self):
        ips = ["127.1.1.1", "127.0.0.1", "192.168.56.1"]
        ips = BootloaderService.remove_local_ips(ips)
        self.assertEqual(["192.168.56.1"], ips)
