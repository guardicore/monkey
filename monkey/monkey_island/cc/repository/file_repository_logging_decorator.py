import logging
from typing import BinaryIO

from . import IFileRepository

logger = logging.getLogger(__name__)


class FileRepositoryLoggingDecorator(IFileRepository):
    """
    An IFileRepository decorator that provides debug logging for other IFileRepositories.
    """

    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository

    def save_file(self, unsafe_file_name: str, file_contents: BinaryIO):
        logger.debug(f"Saving file {unsafe_file_name}")
        return self._file_repository.save_file(unsafe_file_name, file_contents)

    def open_file(self, unsafe_file_name: str) -> BinaryIO:
        logger.debug(f"Opening file {unsafe_file_name}")
        return self._file_repository.open_file(unsafe_file_name)

    def delete_file(self, unsafe_file_name: str):
        logger.debug(f"Deleting file {unsafe_file_name}")
        return self._file_repository.delete_file(unsafe_file_name)

    def delete_files_by_pattern(self, file_name_pattern: str):
        logger.debug(f'Deleting files whose names match the pattern "{file_name_pattern}"')
        return self._file_repository.delete_files_by_pattern(file_name_pattern)

    def delete_all_files(self):
        logger.debug("Deleting all files in the repository")
        return self._file_repository.delete_all_files()
