from __future__ import annotations

import abc
from typing import Iterable

from infection_monkey.telemetry.i_telem import ITelem


class IBatchableTelem(ITelem, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_telemetry_entries(self) -> Iterable:
        pass

    @abc.abstractmethod
    def add_telemetry_to_batch(self, telemetry: IBatchableTelem):
        pass
