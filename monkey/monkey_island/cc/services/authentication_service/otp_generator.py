import string
import time

from common.utils.code_utils import secure_generate_random_string
from monkey_island.cc.services.authentication_service.i_otp_repository import IOTPRepository

OTP_EXPIRATION_TIME = 2 * 60


class OTPGenerator:
    """
    Generates OTPs
    """

    def __init__(self, otp_repository: IOTPRepository):
        self._otp_repository = otp_repository

    def generate_otp(self) -> str:
        """
        Generates a new OTP

        The generated OTP is saved to the `IOTPRepository`
        :return: The generated OTP
        """
        otp_value = self._generate_otp()
        expiration_time = time.monotonic() + OTP_EXPIRATION_TIME
        self._otp_repository.insert_otp(otp_value, expiration_time)

        return otp_value

    def _generate_otp(self) -> str:
        return secure_generate_random_string(32, string.ascii_letters + string.digits + "._-")
