from abc import ABC, abstractmethod

from monkey_island.cc.models import OTP


class IOTPRepository(ABC):
    """A repository used to store and retrieve `OTP`s"""

    @abstractmethod
    def save_otp(self, otp: OTP):
        """
        Insert an OTP into the repository

        :param otp: The OTP to insert
        :raises StorageError: If an error occurs while attempting to insert the OTP
        """

    @abstractmethod
    def get_otp(self, otp: str) -> OTP:
        """
        Get an OTP from the repository

        :param otp: The ID of the OTP to get
        :return: The OTP
        :raises RetrievalError: If an error occurs while attempting to retrieve the OTP
        :raises UnknownRecordError: If the OTP was not found
        """

    @abstractmethod
    def delete_otp(self, otp: str):
        """
        Delete an OTP from the repository

        :param otp: The OTP to delete
        :raises RemovalError: If an error occurs while attempting to delete the OTP
        """

    @abstractmethod
    def reset(self):
        """
        Remove all `OTP`s from the repository

        :raises RemovalError: If an error occurs while attempting to reset the repository
        """
