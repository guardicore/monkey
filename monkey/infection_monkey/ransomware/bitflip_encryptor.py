from pathlib import Path

from infection_monkey.utils import bit_manipulators


class BitflipEncryptor:
    def __init__(self, chunk_size=64):
        self._chunk_size = chunk_size

    def encrypt_file_in_place(self, filepath: Path):
        with open(filepath, "rb+") as f:
            data = f.read(self._chunk_size)
            while data:
                num_bytes_read = len(data)

                encrypted_data = bit_manipulators.flip_bits(data)

                f.seek(-num_bytes_read, 1)
                f.write(encrypted_data)

                data = f.read(self._chunk_size)
