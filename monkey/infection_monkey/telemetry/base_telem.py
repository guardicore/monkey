import abc
import json
import logging

from infection_monkey.control import ControlClient

logger = logging.getLogger(__name__)

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
        data = self.get_data()
        logger.debug("Sending {} telemetry. Data: {}".format(self.telem_category, json.dumps(data)))
        ControlClient.send_telemetry(self.telem_category, data)

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
