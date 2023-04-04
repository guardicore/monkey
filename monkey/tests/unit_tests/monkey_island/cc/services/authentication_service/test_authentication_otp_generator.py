from unittest.mock import MagicMock

from monkey_island.cc.services.authentication_service import AuthenticationOTPGenerator
from monkey_island.cc.services.authentication_service.authentication_facade import (
    AuthenticationFacade,
)


def test_authentication_otp_generator__generates_otp():
    mock_authentication_facade = MagicMock(spec=AuthenticationFacade)

    otp_generator = AuthenticationOTPGenerator(mock_authentication_facade)
    otp_generator.generate_otp()

    assert mock_authentication_facade.generate_otp.called_once
