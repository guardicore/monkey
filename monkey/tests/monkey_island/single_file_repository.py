import io
import re
from typing import BinaryIO, Sequence

from monkey_island.cc import repositories
from monkey_island.cc.repositories import IFileRepository


class SingleFileRepository(IFileRepository):
    def __init__(self):
        self._file = None
        self._file_name = ""

    def get_all_file_names(self) -> Sequence[str]:
        if self._file is None:
            return []

        return [self._file_name]

    def save_file(self, unsafe_file_name: str, file_contents: BinaryIO):
        self._file = io.BytesIO(file_contents.read())
        self._file_name = unsafe_file_name

    def open_file(self, unsafe_file_name: str) -> BinaryIO:
        if self._file is None:
            raise repositories.FileNotFoundError()
        return self._file

    def delete_file(self, unsafe_file_name: str):
        self._file = None
        self._file_name = ""

    def delete_files_by_regex(self, file_name_regex: re.Pattern):
        if re.match(file_name_regex, self._file_name):
            self.delete_file("")

    def delete_all_files(self):
        self.delete_file("")
