from common.types import PercentLimited


class MemoryUtilizer:
    def __init__(self, memory_utilization: PercentLimited):
        self._memory_utilization = memory_utilization

    def start(self):
        pass

    def stop(self):
        pass
