from unittest import TestCase

from common.utils.shellcode_obfuscator import clarify, obfuscate

SHELLCODE = b'1234567890abcd'
OBFUSCATED_SHELLCODE = b'\xc7T\x9a\xf4\xb1cn\x94\xb0X\xf2\xfb^='


class TestShellcodeObfuscator(TestCase):

    def test_obfuscate(self):
        assert obfuscate(SHELLCODE) == OBFUSCATED_SHELLCODE

    def test_clarify(self):
        assert clarify(OBFUSCATED_SHELLCODE) == SHELLCODE
