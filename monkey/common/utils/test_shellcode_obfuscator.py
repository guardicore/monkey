from unittest import TestCase

from common.utils.shellcode_obfuscator import clarify, obfuscate

SHELLCODE_FROM_CMD_PARAM = '\\x52\\x3d\\xf6\\xc9\\x4b\\x5d\\xe0\\x62\\x7e\\x3d\\xa8\\x07\\x7b\\x76\\x30'
OBFUSCATED_PARAM_OUTPUT = '\\x30\\x76\\x7b\\x07\\xa8\\x3d\\x7e\\x62\\xe0\\x5d\\x4b\\xc9\\xf6\\x3d\\x52'
OBFUSCATED_SHELLCODE = "\x30\x76\x7b\x07\xa8\x3d\x7e\x62\xe0\x5d\x4b\xc9\xf6\x3d\x52"
CLARIFIED_SHELLCODE = "\x52\x3d\xf6\xc9\x4b\x5d\xe0\x62\x7e\x3d\xa8\x07\x7b\x76\x30"


class TestShellcodeObfuscator(TestCase):

    def test_obfuscate(self):
        self.assertEqual(obfuscate(SHELLCODE_FROM_CMD_PARAM), OBFUSCATED_PARAM_OUTPUT)

    def test_clarify(self):
        self.assertEqual(clarify(OBFUSCATED_SHELLCODE), CLARIFIED_SHELLCODE)
