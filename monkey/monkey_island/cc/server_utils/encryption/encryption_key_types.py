class EncryptionKey32Bytes(bytes):
    def __init__(self, key: bytes):
        if not isinstance(key, bytes):
            raise TypeError("'key' must be of type 'bytes'")

        if len(key) == 32:
            self.key = key
        else:
            raise ValueError("'key' must be exactly 32 bytes")
