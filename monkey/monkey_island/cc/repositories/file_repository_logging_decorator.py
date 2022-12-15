import logging
import re
from typing import BinaryIO, Sequence

from . import IFileRepository

logger = logging.getLogger(__name__)


class FileRepositoryLoggingDecorator(IFileRepository):
    """
    An IFileRepository decorator that provides debug logging for other IFileRepositories.
    """

    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository

    def get_all_file_names(self) -> Sequence[str]:
        logger.debug("Getting all file names")
        file_names = self._file_repository.get_all_file_names()
        logger.debug(f"Found {len(file_names)} files")

        return file_names

    def save_file(self, unsafe_file_name: str, file_contents: BinaryIO):
        logger.debug(f"Saving file {unsafe_file_name}")
        return self._file_repository.save_file(unsafe_file_name, file_contents)

    def open_file(self, unsafe_file_name: str) -> BinaryIO:
        logger.debug(f"Opening file {unsafe_file_name}")
        return self._file_repository.open_file(unsafe_file_name)

    def delete_file(self, unsafe_file_name: str):
        logger.debug(f"Deleting file {unsafe_file_name}")
        return self._file_repository.delete_file(unsafe_file_name)

    def delete_files_by_regex(self, file_name_regex: re.Pattern):
        logger.debug(f'Deleting files whose names match the regex "{file_name_regex}"')
        return self._file_repository.delete_files_by_regex(file_name_regex)

    def delete_all_files(self):
        logger.debug("Deleting all files in the repository")
        return self._file_repository.delete_all_files()
