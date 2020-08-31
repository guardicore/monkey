# This code is used to obfuscate shellcode
# Usage:
# shellcode_obfuscator.py [your normal shellcode].
# For example:
# shellcode_obfuscator.py "\x52\x3d\xf6\xc9\x4b\x5d\xe0\x62\x7e\x3d\xa8\x07\x7b\x76\x30"
# This returns "\x30\x76\x7b\x07\xa8\x3d\x7e\x62\xe0\x5d\x4b\xc9\xf6\x3d\x52"
# Verify that it's the same shellcode, just reversed and paste it in code.
# Then clarify it before usage to reverse it on runtime.

import sys


def obfuscate(shellcode: str) -> str:
    shellcode = shellcode.split('\\')[::-1]
    return '\\'+'\\'.join(shellcode)[:-1]


def clarify(shellcode: str) -> str:
    return shellcode[::-1]


if __name__ == "__main__":
    print(obfuscate(sys.argv[1]))
