from functools import singledispatch

from infection_monkey.credential_store import ICredentialsStore
from infection_monkey.telemetry.credentials_telem import CredentialsTelem
from infection_monkey.telemetry.i_telem import ITelem
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger


class CredentialsInterceptingTelemetryMessenger(ITelemetryMessenger):
    def __init__(
        self, telemetry_messenger: ITelemetryMessenger, credentials_store: ICredentialsStore
    ):
        self._telemetry_messenger = telemetry_messenger
        self._credentials_store = credentials_store

    def send_telemetry(self, telemetry: ITelem):
        _send_telemetry(telemetry, self._telemetry_messenger, self._credentials_store)


# Note: We can use @singledispatchmethod instead of @singledispatch if we migrate to Python 3.8 or
# later.
@singledispatch
def _send_telemetry(
    telemetry: ITelem,
    telemetry_messenger: ITelemetryMessenger,
    credentials_store: ICredentialsStore,
):
    telemetry_messenger.send_telemetry(telemetry)


@_send_telemetry.register
def _(
    telemetry: CredentialsTelem,
    telemetry_messenger: ITelemetryMessenger,
    credentials_store: ICredentialsStore,
):
    credentials_store.add_credentials(telemetry.credentials)
    telemetry_messenger.send_telemetry(telemetry)
