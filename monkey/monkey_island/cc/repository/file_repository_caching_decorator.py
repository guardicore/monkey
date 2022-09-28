import io
import shutil
from functools import lru_cache
from typing import BinaryIO

from . import IFileRepository


class FileRepositoryCachingDecorator(IFileRepository):
    """
    An IFileRepository decorator that provides caching for other IFileRepositories.
    """

    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository

    def save_file(self, unsafe_file_name: str, file_contents: BinaryIO):
        self._open_file.cache_clear()
        return self._file_repository.save_file(unsafe_file_name, file_contents)

    def open_file(self, unsafe_file_name: str) -> BinaryIO:
        original_file = self._open_file(unsafe_file_name)
        file_copy = io.BytesIO()

        shutil.copyfileobj(original_file, file_copy)
        original_file.seek(0)
        file_copy.seek(0)

        return file_copy

    @lru_cache(maxsize=16)
    def _open_file(self, unsafe_file_name: str) -> BinaryIO:
        return self._file_repository.open_file(unsafe_file_name)

    def delete_file(self, unsafe_file_name: str):
        self._open_file.cache_clear()
        return self._file_repository.delete_file(unsafe_file_name)

    def delete_files_by_pattern(self, file_name_pattern: str):
        self._open_file.cache_clear()
        return self._file_repository.delete_files_by_pattern(file_name_pattern)

    def delete_all_files(self):
        self._open_file.cache_clear()
        return self._file_repository.delete_all_files()
