import abc


class ITelem(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def send(self, log_data=True):
        """
        Sends telemetry to island
        """

    @abc.abstractmethod
    def get_data(self) -> dict:
        """
        :return: Data of telemetry (should be dict)
        """
        pass

    @property
    @abc.abstractmethod
    def json_encoder(self):
        pass

    @property
    @abc.abstractmethod
    def telem_category(self):
        """
        :return: Telemetry type
        """
        pass
