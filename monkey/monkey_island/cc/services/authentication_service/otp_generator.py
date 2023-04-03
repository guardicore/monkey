from .authentication_facade import AuthenticationFacade


class OTPGenerator:
    """
    Generates OTPs
    """

    def __init__(self, authentication_facade: AuthenticationFacade):
        self._authentication_facade = authentication_facade

    def generate_otp(self) -> str:
        """
        Generates a new OTP
        """
        return self._authentication_facade.generate_otp()
