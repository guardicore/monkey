import abc

from infection_monkey.control import ControlClient

__author__ = 'itay.mizeretz'


class BaseTelem(object):
    """
    Abstract base class for telemetry.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    def send(self):
        """
        Sends telemetry to island
        """
        ControlClient.send_telemetry(self.telem_category, self.get_data())

    @abc.abstractproperty
    def telem_category(self):
        """
        :return: Telemetry type
        """
        pass

    @abc.abstractmethod
    def get_data(self):
        """
        :return: Data of telemetry (should be dict)
        """
        pass
