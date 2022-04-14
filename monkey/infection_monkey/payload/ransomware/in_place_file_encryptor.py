import re
from pathlib import Path
from typing import Callable

FILE_EXTENSION_REGEX = re.compile(r"^\.[^\\/]+$")


class InPlaceFileEncryptor:
    def __init__(
        self,
        encrypt_bytes: Callable[[bytes], bytes],
        new_file_extension: str = "",
        chunk_size: int = 64,
    ):
        self._encrypt_bytes = encrypt_bytes
        self._chunk_size = chunk_size

        if new_file_extension and not FILE_EXTENSION_REGEX.match(new_file_extension):
            raise ValueError(f'"{new_file_extension}" is not a valid file extension.')

        self._new_file_extension = new_file_extension

    def __call__(self, filepath: Path):
        self._encrypt_file(filepath)

        if self._new_file_extension:
            self._add_extension(filepath)

    def _encrypt_file(self, filepath: Path):
        with open(filepath, "rb+") as f:
            for data in iter(lambda: f.read(self._chunk_size), b""):
                encrypted_data = self._encrypt_bytes(data)

                f.seek(-len(encrypted_data), 1)
                f.write(encrypted_data)

    def _add_extension(self, filepath: Path):
        new_filepath = filepath.with_suffix(f"{filepath.suffix}{self._new_file_extension}")
        filepath.rename(new_filepath)
