import abc
from typing import BinaryIO


class FileRetrievalError(ValueError):
    pass


class IFileStorageService(metaclass=abc.ABCMeta):
    """
    A service that allows the storage and retrieval of individual files.
    """

    @abc.abstractmethod
    def save_file(self, unsafe_file_name: str, file_contents: BinaryIO):
        """
        Save a file, identified by a name

        :param unsafe_file_name: An unsanitized file name that will identify the file
        :param file_contents: The data to be stored in the file
        """
        pass

    @abc.abstractmethod
    def open_file(self, unsafe_file_name: str) -> BinaryIO:
        """
        Open a file and return a file-like object

        :param unsafe_file_name: An unsanitized file name that identifies the file to be opened
        :return: A file-like object providing access to the file's contents
        :rtype: io.BinaryIO
        :raises FileRetrievalError: if the file cannot be opened
        """
        pass

    @abc.abstractmethod
    def delete_file(self, unsafe_file_name: str):
        """
        Delete a file

        This method will delete the file specified by `unsafe_file_name`. This operation is
        idempotent and will succeed if the file to be deleted does not exist.

        :param unsafe_file_name: An unsanitized file name that identifies the file to be deleted
        """
        pass

    @abc.abstractmethod
    def delete_all_files(self):
        """
        Delete all files that have been stored using this service.
        """
        pass
