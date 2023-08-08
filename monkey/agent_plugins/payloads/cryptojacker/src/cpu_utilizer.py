from typing import Optional

from common.types import PercentLimited


class CPUUtilizer:
    def __init__(self, cpu_utilization: PercentLimited):
        self._cpu_utilization = cpu_utilization

    def start(self):
        pass

    def stop(self, timeout: Optional[float] = None):
        pass
