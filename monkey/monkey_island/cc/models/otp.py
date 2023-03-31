from datetime import datetime

from common.base_models import InfectionMonkeyBaseModel


class OTP(InfectionMonkeyBaseModel):
    """Represents a one-time password (OTP)"""

    otp: str
    """One-time password (OTP)"""

    expiration_time: datetime
    """The OTP is no longer valid after this time"""
