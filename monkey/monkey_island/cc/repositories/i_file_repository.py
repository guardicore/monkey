import abc
import re
from typing import BinaryIO, Sequence

from monkey_island.cc.repositories import UnknownRecordError


# TODO: Remove this and use UnknownRecordError directly wherever needed.
class FileNotFoundError(UnknownRecordError):
    pass


class IFileRepository(metaclass=abc.ABCMeta):
    """
    A service that allows the storage and retrieval of individual files.
    """

    @abc.abstractmethod
    def get_all_file_names(self) -> Sequence[str]:
        """
        Return the names of all files in the repository

        :return: The names of all files in the repository
        :raises RetrievalError: If an error occurs while attempting get all file names
        """

    @abc.abstractmethod
    def save_file(self, unsafe_file_name: str, file_contents: BinaryIO):
        """
        Save a file, identified by a name

        :param unsafe_file_name: An unsanitized file name that will identify the file
        :param file_contents: The data to be stored in the file
        :raises StorageError: If an error was encountered while attempting to store the file
        """
        pass

    @abc.abstractmethod
    def open_file(self, unsafe_file_name: str) -> BinaryIO:
        """
        Open a file and return a read-only file-like object

        :param unsafe_file_name: An unsanitized file name that identifies the file to be opened
        :return: A file-like object providing access to the file's contents
        :raises FileNotFoundError: if the file does not exist
        :raises RetrievalError: if the file exists but cannot be retrieved
        """
        pass

    @abc.abstractmethod
    def delete_file(self, unsafe_file_name: str):
        """
        Delete a file

        This method will delete the file specified by `unsafe_file_name`. This operation is
        idempotent and will succeed if the file to be deleted does not exist.

        :param unsafe_file_name: An unsanitized file name that identifies the file to be deleted
        :raises RemovalError: If an error was encountered while attempting to remove a file
        """
        pass

    @abc.abstractmethod
    def delete_files_by_regex(self, file_name_regex: re.Pattern):
        """
        Delete files whose names match a particular regex

        This method matches relevant files and deletes them using `delete_file()`.

        :param file_name_regex: A regex with which a file's name should match before deleting it
        """
        pass

    @abc.abstractmethod
    def delete_all_files(self):
        """
        Delete all files that have been stored using this service.

        :raises RemovalError: If an error was encountered while attempting to remove a file
        """
        pass
