import threading

from common.types import PercentLimited


class CPUUtilizer:
    def __init__(self, cpu_utilization: PercentLimited):
        self._cpu_utilization = cpu_utilization

    def __call__(self, interrupt: threading.Event):
        pass
