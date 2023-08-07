import threading

from common.types import PercentLimited


class MemoryUtilizer:
    def __init__(self, memory_utilization: PercentLimited):
        self._memory_utilization = memory_utilization

    def __call__(self, interrupt: threading.Event):
        pass
