from unittest.mock import MagicMock

from common.credentials import Credentials, Password, SSHKeypair, Username
from infection_monkey.telemetry.credentials_telem import CredentialsTelem
from infection_monkey.telemetry.messengers.credentials_intercepting_telemetry_messenger import (
    CredentialsInterceptingTelemetryMessenger,
)

TELEM_CREDENTIALS = [
    Credentials(
        Username("user1"),
        SSHKeypair(public_key="some_public_key", private_key="some_private_key"),
    ),
    Credentials(Username("root"), Password("password")),
]


class MockCredentialsTelem(CredentialsTelem):
    def __init(self, credentials):
        super().__init__(credentials)

    def get_data(self):
        return {}


def test_credentials_generic_telemetry(TestTelem):
    mock_telemetry_messenger = MagicMock()
    mock_credentials_repository = MagicMock()

    telemetry_messenger = CredentialsInterceptingTelemetryMessenger(
        mock_telemetry_messenger, mock_credentials_repository
    )

    telemetry_messenger.send_telemetry(TestTelem())

    assert mock_telemetry_messenger.send_telemetry.called
    assert not mock_credentials_repository.add_credentials.called


def test_successful_intercepting_credentials_telemetry():
    mock_telemetry_messenger = MagicMock()
    mock_credentials_repository = MagicMock()
    mock_empty_credentials_telem = MockCredentialsTelem(TELEM_CREDENTIALS)

    telemetry_messenger = CredentialsInterceptingTelemetryMessenger(
        mock_telemetry_messenger, mock_credentials_repository
    )

    telemetry_messenger.send_telemetry(mock_empty_credentials_telem)

    assert mock_telemetry_messenger.send_telemetry.called
    assert mock_credentials_repository.add_credentials.called
