import logging
import shutil
from pathlib import Path
from typing import BinaryIO

from common.utils.file_utils import get_all_regular_files_in_directory
from monkey_island.cc.server_utils.file_utils import create_secure_directory

from . import FileRetrievalError, IFileStorageService

logger = logging.getLogger(__name__)


class DirectoryFileStorageService(IFileStorageService):
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

    def save_file(self, unsafe_file_name: str, file_contents: BinaryIO):
        safe_file_path = self._get_safe_file_path(unsafe_file_name)

        logger.debug(f"Saving file contents to {safe_file_path}")
        with open(safe_file_path, "wb") as dest:
            shutil.copyfileobj(file_contents, dest)

    def open_file(self, unsafe_file_name: str) -> BinaryIO:
        safe_file_path = self._get_safe_file_path(unsafe_file_name)

        try:
            logger.debug(f"Opening {safe_file_path}")
            return open(safe_file_path, "rb")
        except OSError as err:
            logger.error(err)
            raise FileRetrievalError(f"Failed to retrieve file {safe_file_path}: {err}") from err

    def delete_file(self, unsafe_file_name: str):
        safe_file_path = self._get_safe_file_path(unsafe_file_name)

        try:
            logger.debug(f"Deleting {safe_file_path}")
            safe_file_path.unlink()
        except FileNotFoundError:
            # This method is idempotent.
            pass

    def _get_safe_file_path(self, unsafe_file_name: str):
        # Remove any path information from the file name.
        safe_file_name = Path(unsafe_file_name).resolve().name
        safe_file_path = (self._storage_directory / safe_file_name).resolve()

        # This is a paranoid check to avoid directory traversal attacks.
        if self._storage_directory.resolve() not in safe_file_path.parents:
            raise ValueError(f"The file named {unsafe_file_name} can not be safely retrieved")

        logger.debug(f"Untrusted file name {unsafe_file_name} sanitized: {safe_file_path}")
        return safe_file_path

    def delete_all_files(self):
        for file in get_all_regular_files_in_directory(self._storage_directory):
            logger.debug(f"Deleting {file}")
            file.unlink()
