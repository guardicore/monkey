import abc
import threading
from typing import Dict


class IPayload(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, options: Dict, interrupt: threading.Event):
        """
        Runs the payload
        :param Dict options: A dictionary containing options that modify the behavior of the payload
        :param threading.Event interrupt: A threading.Event object that signals the payload to stop
                                          executing and clean itself up.
        """
