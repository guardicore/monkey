from abc import ABC, abstractmethod

from .types import OTP


class IOTPGenerator(ABC):
    """Generator for OTPs"""

    @abstractmethod
    def generate_otp(self) -> OTP:
        """
        Generates a new OTP
        """
