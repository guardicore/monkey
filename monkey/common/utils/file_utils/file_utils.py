import io
import logging
import shutil
from pathlib import Path
from typing import BinaryIO

logger = logging.getLogger(__name__)


def get_text_file_contents(file_path: Path) -> str:
    with open(file_path, "rt") as f:
        file_contents = f.read()
    return file_contents


def make_fileobj_copy(src: BinaryIO) -> BinaryIO:
    """
    Creates a file-like object that is a copy of the provided file-like object

    The source file-like object is reset to position 0 and a copy is made. Both the source file and
    the copy are reset to position 0 before returning.

    :param src: A file-like object to copy
    :return: A file-like object that is a copy of the provided file-like object
    """
    dst = io.BytesIO()

    src.seek(0)
    shutil.copyfileobj(src, dst)

    src.seek(0)
    dst.seek(0)

    return dst


def append_bytes(file: BinaryIO, bytes_to_append: bytes) -> BinaryIO:
    starting_position = file.tell()

    file.seek(0, io.SEEK_END)
    file.write(bytes_to_append)
    file.seek(starting_position, io.SEEK_SET)

    return file
