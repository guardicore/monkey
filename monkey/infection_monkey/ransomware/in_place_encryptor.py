from pathlib import Path
from typing import Callable


class InPlaceEncryptor:
    def __init__(self, encrypt_bytes: Callable[[bytes], bytes], chunk_size: int = 64):
        self._encrypt_bytes = encrypt_bytes
        self._chunk_size = chunk_size

    def __call__(self, filepath: Path):
        with open(filepath, "rb+") as f:
            data = f.read(self._chunk_size)
            while data:
                num_bytes_read = len(data)

                encrypted_data = self._encrypt_bytes(data)

                f.seek(-num_bytes_read, 1)
                f.write(encrypted_data)

                data = f.read(self._chunk_size)
