import abc
import json
import logging

from infection_monkey.control import ControlClient

logger = logging.getLogger(__name__)

__author__ = 'itay.mizeretz'


class BaseTelem(object, metaclass=abc.ABCMeta):
    """
    Abstract base class for telemetry.
    """

    def __init__(self):
        pass

    def send(self, log_data=True):
        """
        Sends telemetry to island
        """
        data = self.get_data()
        if log_data:
            data_to_log = json.dumps(data)
        else:
            data_to_log = 'redacted'
        logger.debug("Sending {} telemetry. Data: {}".format(self.telem_category, data_to_log))
        ControlClient.send_telemetry(self.telem_category, data)

    @property
    @abc.abstractmethod
    def telem_category(self):
        """
        :return: Telemetry type
        """
        pass

    @abc.abstractmethod
    def get_data(self) -> dict:
        """
        :return: Data of telemetry (should be dict)
        """
        pass
