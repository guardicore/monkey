import io
import re
from typing import BinaryIO, Dict, Sequence

from monkeytoolbox import del_key

from monkey_island.cc.repositories import IFileRepository, UnknownRecordError


class InMemoryFileRepository(IFileRepository):
    def __init__(self):
        self._files: Dict[str, bytes] = {}

    def get_all_file_names(self) -> Sequence[str]:
        return list(self._files.keys())

    def save_file(self, unsafe_file_name: str, file_contents: BinaryIO):
        self._files[unsafe_file_name] = file_contents.read()

    def open_file(self, unsafe_file_name: str) -> BinaryIO:
        try:
            return io.BytesIO(self._files[unsafe_file_name])
        except KeyError:
            raise UnknownRecordError(f"Unknown file {unsafe_file_name}")

    def delete_file(self, unsafe_file_name: str):
        del_key(self._files, unsafe_file_name)

    def delete_files_by_regex(self, file_name_regex: re.Pattern):
        self._files = {
            name: contents
            for name, contents in self._files.items()
            if not re.match(file_name_regex, name)
        }

    def delete_all_files(self):
        self._files = {}
