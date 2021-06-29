from infection_monkey.telemetry.i_telem import ITelem
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger


class LegacyTelemetryMessengerAdapter(ITelemetryMessenger):
    """
    Provides an adapter between modules that require an ITelemetryMessenger and the
    legacy method for sending telemetry.
    """

    def send_telemetry(self, telemetry: ITelem):
        telemetry.send()
