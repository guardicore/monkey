import logging
import os
import re
import shutil
from pathlib import Path
from typing import BinaryIO, Sequence

from monkeytoolbox import create_secure_directory, get_all_regular_files_in_directory

from monkey_island.cc import repositories
from monkey_island.cc.repositories import RemovalError, RetrievalError, StorageError

from . import IFileRepository

logger = logging.getLogger(__name__)


class LocalStorageFileRepository(IFileRepository):
    """
    A implementation of IFileStorageService that reads and writes files from/to the local
    filesystem.
    """

    def __init__(self, storage_directory: Path):
        """
        :param storage_directory: A Path object representing the directory where files will be
                                  stored. If the directory does not exist, it will be created.
        """
        if storage_directory.exists() and not storage_directory.is_dir():
            raise ValueError(f"The provided path must point to a directory: {storage_directory}")

        if not storage_directory.exists():
            create_secure_directory(storage_directory)

        self._storage_directory = storage_directory

    def get_all_file_names(self) -> Sequence[str]:
        try:
            return [
                file.name for file in get_all_regular_files_in_directory(self._storage_directory)
            ]
        except Exception as err:
            raise RetrievalError(f"Error while attempting to get all file names: {err}")

    def save_file(self, unsafe_file_name: str, file_contents: BinaryIO):
        try:
            safe_file_path = self._get_safe_file_path(unsafe_file_name)

            with open(safe_file_path, "wb") as dest:
                shutil.copyfileobj(file_contents, dest)
        except Exception as err:
            raise StorageError(f"Error while attempting to store {unsafe_file_name}: {err}")

    def open_file(self, unsafe_file_name: str) -> BinaryIO:
        try:
            safe_file_path = self._get_safe_file_path(unsafe_file_name)
            return open(safe_file_path, "rb")
        except FileNotFoundError as err:
            # Wrap Python's FileNotFound error, which is-an OSError,
            # in repositories.FileNotFoundError
            raise repositories.FileNotFoundError(
                f'The requested file "{unsafe_file_name}" does not exist: {err}'
            )
        except Exception as err:
            raise RetrievalError(
                f'Error retrieving file "{unsafe_file_name}" from the repository: {err}'
            )

    def delete_files_by_regex(self, file_name_regex: re.Pattern):
        for file_name in os.listdir(self._storage_directory):
            if re.match(file_name_regex, file_name):
                self.delete_file(file_name)

    def delete_file(self, unsafe_file_name: str):
        try:
            safe_file_path = self._get_safe_file_path(unsafe_file_name)
            safe_file_path.unlink()
        except FileNotFoundError:
            # This method is idempotent.
            pass
        except Exception as err:
            raise RemovalError(f"Error while attempting to remove {unsafe_file_name}: {err}")

    def _get_safe_file_path(self, unsafe_file_name: str):
        # Remove any path information from the file name.
        safe_file_name = Path(unsafe_file_name).resolve().name
        safe_file_path = (self._storage_directory / safe_file_name).resolve()

        # This is a paranoid check to avoid directory traversal attacks.
        if self._storage_directory.resolve() not in safe_file_path.parents:
            raise ValueError(
                f'The file named "{unsafe_file_name}" cannot be safely retrieved or written'
            )

        logger.debug(f"Untrusted file name {unsafe_file_name} sanitized: {safe_file_path}")
        return safe_file_path

    def delete_all_files(self):
        try:
            for file in get_all_regular_files_in_directory(self._storage_directory):
                logger.debug(f"Deleting {file}")
                file.unlink()
        except Exception as err:
            raise RemovalError(f"Error while attempting to clear the repository: {err}")
