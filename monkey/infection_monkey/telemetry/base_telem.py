import abc
import json
import logging

from infection_monkey.control import ControlClient

logger = logging.getLogger(__name__)
LOGGED_DATA_LENGTH = 300  # How many characters of telemetry data will be logged

__author__ = "itay.mizeretz"


# TODO: Rework the interface for telemetry; this class has too many responsibilities
#       (i.e. too many reasons to change):
#
#       1. Store telemetry data
#       2. Serialize telemetry data
#       3. Send telemetry data
#       4. Log telemetry data
#
#       One appaoach is that Telemetry objects should be immutable after construction
#       and the only necessary public method be a `serialize()` method. Telemetry
#       objects can be passed to other objects or functions that are responsible for
#       logging and sending them.


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
        serialized_data = json.dumps(data, cls=self.json_encoder)
        self._log_telem_sending(serialized_data, log_data)
        ControlClient.send_telemetry(self.telem_category, serialized_data)

    @abc.abstractmethod
    def get_data(self) -> dict:
        """
        :return: Data of telemetry (should be dict)
        """
        pass

    @property
    def json_encoder(self):
        return json.JSONEncoder

    def _log_telem_sending(self, serialized_data: str, log_data=True):
        logger.debug(f"Sending {self.telem_category} telemetry.")
        if log_data:
            logger.debug(f"Telemetry contents: {BaseTelem._truncate_data(serialized_data)}")

    @property
    @abc.abstractmethod
    def telem_category(self):
        """
        :return: Telemetry type
        """
        pass

    @staticmethod
    def _truncate_data(data: str):
        if len(data) <= LOGGED_DATA_LENGTH:
            return data
        else:
            return f"{data[:LOGGED_DATA_LENGTH]}..."
