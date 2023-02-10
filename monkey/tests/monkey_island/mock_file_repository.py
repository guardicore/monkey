import io
import re
from typing import BinaryIO, Sequence

from monkey_island.cc import repositories
from monkey_island.cc.repositories import IFileRepository

FILE_NAME = "test_file"
FILE_CONTENTS = b"HelloWorld!"


class MockFileRepository(IFileRepository):
    def __init__(self):
        self._file = io.BytesIO(FILE_CONTENTS)

    def get_all_file_names(self) -> Sequence[str]:
        return [FILE_NAME]

    def save_file(self, unsafe_file_name: str, file_contents: BinaryIO):
        pass

    def open_file(self, unsafe_file_name: str) -> BinaryIO:
        if unsafe_file_name != FILE_NAME:
            raise repositories.FileNotFoundError()

        return self._file

    def delete_file(self, unsafe_file_name: str):
        pass

    def delete_files_by_regex(self, file_name_regex: re.Pattern):
        pass

    def delete_all_files(self):
        pass
