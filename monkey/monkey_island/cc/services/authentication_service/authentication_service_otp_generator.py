from monkeytypes import OTP

from .authentication_facade import AuthenticationFacade
from .i_otp_generator import IOTPGenerator


class AuthenticationServiceOTPGenerator(IOTPGenerator):
    """
    Generates OTPs
    """

    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    def generate_otp(self) -> OTP:
        """
        Generates a new OTP
        """
        return self._authentication_facade.generate_otp()
