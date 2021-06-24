import abc

from infection_monkey.telemetry.base_telem import BaseTelem


class ITelemetryMessenger(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def send_telemetry(self, telemetry: BaseTelem):
        pass
