from infection_monkey.telemetry.base_telem import BaseTelem
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger


class TelemetryMessengerWrapper(ITelemetryMessenger):
    def send_telemetry(self, telemetry: BaseTelem):
        telemetry.send()
