import time
from unittest.mock import MagicMock

from monkey_island.cc.services.authentication_service.i_otp_repository import IOTPRepository
from monkey_island.cc.services.authentication_service.otp import OTP_EXPIRATION_TIME, OTPGenerator


def test_otp_generator__saves_otp():
    mock_otp_repository = MagicMock(spec=IOTPRepository)

    otp_generator = OTPGenerator(mock_otp_repository)
    otp = otp_generator.generate_otp()

    assert mock_otp_repository.insert_otp.called_once_with(otp)


def test_otp_generator__uses_expected_expiration_time(freezer):
    mock_otp_repository = MagicMock(spec=IOTPRepository)
    otp_generator = OTPGenerator(mock_otp_repository)

    otp_generator.generate_otp()

    expiration_time = mock_otp_repository.insert_otp.call_args[0][1]
    expected_expiration_time = time.monotonic() + OTP_EXPIRATION_TIME
    assert expiration_time == expected_expiration_time
