class SizeError(Exception):
    """
    Raised when an argument is not of the expected size during object creation.
    """

    pass


class EncryptionKey32Bytes(bytes):
    def __init__(self, key: bytes):
        if len(key) == 32:
            self.key = key
        else:
            raise SizeError("Key size should be 32 bytes.")
