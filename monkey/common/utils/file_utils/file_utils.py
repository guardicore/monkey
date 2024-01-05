import io
from typing import BinaryIO


def append_bytes(file: BinaryIO, bytes_to_append: bytes) -> BinaryIO:
    starting_position = file.tell()

    file.seek(0, io.SEEK_END)
    file.write(bytes_to_append)
    file.seek(starting_position, io.SEEK_SET)

    return file
