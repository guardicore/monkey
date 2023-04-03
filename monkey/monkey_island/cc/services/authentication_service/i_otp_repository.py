from abc import ABC, abstractmethod

from .types import OTP


class IOTPRepository(ABC):
    """A repository used to store and retrieve `OTP`s"""

    @abstractmethod
    def insert_otp(self, otp: OTP, expiration: float):
        """
        Insert an OTP into the repository

        :param otp: The OTP to insert
        :param expiration: The time that the OTP expires
        :raises StorageError: If an error occurs while attempting to insert the OTP
        """

    @abstractmethod
    def get_expiration(self, otp: OTP) -> float:
        """
        Get the expiration time of a given OTP

        :param otp: OTP for which to get the expiration time
        :return: The time that the OTP expires
        :raises RetrievalError: If an error occurs while attempting to retrieve the expiration time
        :raises UnknownRecordError: If the OTP was not found
        """

    @abstractmethod
    def reset(self):
        """
        Remove all `OTP`s from the repository

        :raises RemovalError: If an error occurs while attempting to reset the repository
        """
