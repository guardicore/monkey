from infection_monkey.telemetry.i_telem import ITelem
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger


class TelemetryMessengerWrapper(ITelemetryMessenger):
    def send_telemetry(self, telemetry: ITelem):
        telemetry.send()
