import abc

from infection_monkey.control import ControlClient
import logging

__author__ = 'itay.mizeretz'

LOG = logging.getLogger(__name__)


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
        ControlClient.send_telemetry(self.telem_type, self.get_data())

    @abc.abstractproperty
    def telem_type(self):
        """
        :return: Telemetry type
        """
        pass

    @abc.abstractmethod
    def get_data(self):
        """
        :return: Telemetry type
        """
        pass
