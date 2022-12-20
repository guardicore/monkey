import abc
from typing import Dict

from common.types import Event


class IPayload(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, options: Dict, interrupt: Event):
        """
        Runs the payload
        :param Dict options: A dictionary containing options that modify the behavior of the payload
        :param `Event` interrupt: An `Event` object that signals the payload to stop executing and
                                  clean itself up.
        """
