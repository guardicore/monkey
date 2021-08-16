import abc

from infection_monkey.telemetry.i_telem import ITelem


class ITelemetryMessenger(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def send_telemetry(self, telemetry: ITelem):
        pass
