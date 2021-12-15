import pytest

from infection_monkey.telemetry.i_telem import ITelem
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger


class TelemetryMessengerSpy(ITelemetryMessenger):
    def __init__(self):
        self.telemetries = []

    def send_telemetry(self, telemetry: ITelem):
        self.telemetries.append(telemetry)


@pytest.fixture
def telemetry_messenger_spy():
    return TelemetryMessengerSpy()


@pytest.fixture
def automated_master_config(load_monkey_config):
    return load_monkey_config("automated_master_config.json")
