class EncryptionKey32Bytes(bytes):
    def __init__(self, key: bytes):
        if not isinstance(key, bytes):
            raise TypeError("Key is not of type `bytes`")
        if len(key) == 32:
            self.key = key
        else:
            raise ValueError("Key size should be 32 bytes")
