from unittest.mock import MagicMock

from infection_monkey.credential_collectors import Password, SSHKeypair, Username
from infection_monkey.credential_store import AggregatingCredentialsStore
from infection_monkey.i_puppet import Credentials
from infection_monkey.telemetry.base_telem import BaseTelem
from infection_monkey.telemetry.credentials_telem import CredentialsTelem
from infection_monkey.telemetry.messengers.credentials_intercepting_telemetry_messenger import (
    CredentialsInterceptingTelemetryMessenger,
)

TELEM_CREDENTIALS = [
    Credentials(
        [Username("user1"), Username("user3")],
        [
            Password("abcdefg"),
            Password("root"),
            SSHKeypair(public_key="some_public_key", private_key="some_private_key"),
        ],
    )
]


class TestTelem(BaseTelem):
    telem_category = None
    __test__ = False

    def __init__(self):
        pass

    def get_data(self):
        return {}


class MockCredentialsTelem(CredentialsTelem):
    def __init(self, credentials):
        super().__init__(credentials)

    def get_data(self):
        return {}


def test_credentials_generic_telemetry():
    mock_telemetry_messenger = MagicMock()
    mock_credentials_store = MagicMock()

    telemetry_messenger = CredentialsInterceptingTelemetryMessenger(
        mock_telemetry_messenger, mock_credentials_store
    )

    telemetry_messenger.send_telemetry(TestTelem())

    assert mock_telemetry_messenger.send_telemetry.called
    assert not mock_credentials_store.add_credentials.called


def test_successful_intercepting_credentials_telemetry():
    mock_telemetry_messenger = MagicMock()
    aggregating_credentials_store = AggregatingCredentialsStore(MagicMock())
    mock_empty_credentials_telem = MockCredentialsTelem([])

    telemetry_messenger = CredentialsInterceptingTelemetryMessenger(
        mock_telemetry_messenger, aggregating_credentials_store
    )

    telemetry_messenger.send_telemetry(mock_empty_credentials_telem)

    assert mock_telemetry_messenger.send_telemetry.called
    assert not aggregating_credentials_store.stored_credentials

    mock_credentials_telem = MockCredentialsTelem(TELEM_CREDENTIALS)
    telemetry_messenger.send_telemetry(mock_credentials_telem)

    assert aggregating_credentials_store.stored_credentials
