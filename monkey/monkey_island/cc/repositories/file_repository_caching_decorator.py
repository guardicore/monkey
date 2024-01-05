import re
from functools import lru_cache
from typing import BinaryIO, Optional, Sequence

from monkeytoolbox import make_fileobj_copy

from . import IFileRepository


class FileRepositoryCachingDecorator(IFileRepository):
    """
    An IFileRepository decorator that provides caching for other IFileRepositories.
    """

    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository
        self._all_file_names_cache: Optional[Sequence[str]] = None

    def get_all_file_names(self) -> Sequence[str]:
        if self._all_file_names_cache is not None:
            return self._all_file_names_cache

        self._all_file_names_cache = self._file_repository.get_all_file_names()
        return self._all_file_names_cache

    def save_file(self, unsafe_file_name: str, file_contents: BinaryIO):
        self._clear_caches()
        return self._file_repository.save_file(unsafe_file_name, file_contents)

    def open_file(self, unsafe_file_name: str) -> BinaryIO:
        original_file = self._open_file(unsafe_file_name)

        return make_fileobj_copy(original_file)

    @lru_cache(maxsize=16)
    def _open_file(self, unsafe_file_name: str) -> BinaryIO:
        return self._file_repository.open_file(unsafe_file_name)

    def delete_file(self, unsafe_file_name: str):
        self._clear_caches()
        return self._file_repository.delete_file(unsafe_file_name)

    def delete_files_by_regex(self, file_name_regex: re.Pattern):
        self._clear_caches()
        return self._file_repository.delete_files_by_regex(file_name_regex)

    def delete_all_files(self):
        self._clear_caches()
        return self._file_repository.delete_all_files()

    def _clear_caches(self):
        self._open_file.cache_clear()
        self._clear_get_all_file_names_cache()

    def _clear_get_all_file_names_cache(self):
        self._all_file_names_cache = None
