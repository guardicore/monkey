from typing import BinaryIO

from monkey_island.cc.repositories import RetrievalError

from . import MockFileRepository


class OpenErrorFileRepository(MockFileRepository):
    def open_file(self, unsafe_file_name: str) -> BinaryIO:
        raise RetrievalError("Error retrieving file")
