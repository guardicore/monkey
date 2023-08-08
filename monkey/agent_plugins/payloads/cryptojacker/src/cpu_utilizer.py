import logging
from typing import Optional

from common.types import PercentLimited
from infection_monkey.utils.threading import create_daemon_thread

from .cryptojacker import THREAD_JOIN_TIMEOUT

logger = logging.getLogger(__name__)


class CPUUtilizer:
    def __init__(self, cpu_utilization: PercentLimited):
        self._cpu_utilizer_thread = create_daemon_thread(
            target=self._utilize_cpu,
            name="CPUUtilizationThread",
            args=(cpu_utilization,),
        )

    def start(self):
        logger.info("Utilizing CPU")
        self._cpu_utilizer_thread.start()

    def _utilize_cpu(self, cpu_utilization: PercentLimited):
        pass

    def stop(self, timeout: Optional[float] = None):
        logger.info("Stopping CPU utilization")
        self._cpu_utilizer_thread.join(THREAD_JOIN_TIMEOUT)
        if self._cpu_utilizer_thread.is_alive():
            logger.info(
                "Timed out while waiting for CPU utilization thread to stop, "
                "it will be stopped forcefully when the parent process terminates"
            )
