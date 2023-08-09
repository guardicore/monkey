import hashlib
import logging
from typing import Optional
import threading
from random import randbytes  # noqa: DUO102 (this isn't for cryptographic use)
from typing import Optional

import psutil

from common.types import NonNegativeFloat, PercentLimited
from infection_monkey.utils.threading import create_daemon_thread

logger = logging.getLogger(__name__)


ACCURACY_THRESHOLD = 0.02
INITIAL_SLEEP_SECONDS = 0.001
AVERAGE_BLOCK_SIZE_BYTES = int(
    3.25 * 1024 * 1024
)  # 3.25 MB - Source: https://trustmachines.co/blog/bitcoin-ordinals-reignited-block-size-debate/
OPERATION_COUNT = 250
OPERATION_COUNT_MODIFIER_START = int(OPERATION_COUNT / 10)
OPERATION_COUNT_MODIFIER_FACTOR = 1.5
MINIMUM_SLEEP = 0.000001


class CPUUtilizer:
    def __init__(self, target_cpu_utilization_percent: PercentLimited):
        target_cpu_utilization = target_cpu_utilization_percent.as_decimal_fraction()

        self._should_stop_cpu_utilization = threading.Event()
        self._cpu_utilizer_thread = create_daemon_thread(
            target=self._utilize_cpu,
            name="CPUUtilizationThread",
            args=(target_cpu_utilization,),
        )

    def start(self):
        logger.info("Utilizing CPU")

        self._cpu_utilizer_thread.start()

    def _utilize_cpu(self, target_cpu_utilization: NonNegativeFloat):
        operation_count_modifier = OPERATION_COUNT_MODIFIER_START
        sleep_seconds = INITIAL_SLEEP_SECONDS if target_cpu_utilization < 1.0 else 0
        block = randbytes(AVERAGE_BLOCK_SIZE_BYTES)
        nonce = 0

        process = psutil.Process()
        # This is a throw-away call. The first call to cpu_percent() always returns 0, even
        # after generating some hashes.
        # https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent
        process.cpu_percent()

        while not self._should_stop_cpu_utilization.is_set():
            # The operation_count_modifier decreases the number of hashes per iteration.
            # The modifier, itself, decreases by a factor of 1.5 each iteration, until
            # it reaches 1. This allows a higher sample rate of the CPU utilization
            # early on to help the sleep time to converge quicker.
            for _ in range(0, int(OPERATION_COUNT / operation_count_modifier)):
                digest = hashlib.sha256()
                digest.update(nonce.to_bytes(8))
                digest.update(block)
                nonce += 1

                self._should_stop_cpu_utilization.wait(sleep_seconds)

            operation_count_modifier = max(
                int(operation_count_modifier / OPERATION_COUNT_MODIFIER_FACTOR), 1
            )

            measured_cpu_utilization = process.cpu_percent() / 100
            cpu_utilization_percent_error = CPUUtilizer._calculate_percent_error(
                measured=measured_cpu_utilization, target=target_cpu_utilization
            )

            sleep_seconds = CPUUtilizer._calculate_new_sleep(
                sleep_seconds, cpu_utilization_percent_error
            )

    @staticmethod
    def _calculate_percent_error(measured: float, target: float) -> float:
        return (measured - target) / target

    @staticmethod
    def _calculate_new_sleep(current_sleep: float, percent_error: float):
        if abs(percent_error) < ACCURACY_THRESHOLD:
            return current_sleep

        # Since our multiplication is based on sleep_seconds, don't ever let sleep_seconds == 0,
        # otherwise it will never equal anything else. CAVEAT: If the target utilization is 100%,
        # current_sleep will be initialized to 0.
        return current_sleep * max((1 + percent_error), MINIMUM_SLEEP)

    def stop(self, timeout: Optional[float] = None):
        logger.info("Stopping CPU utilization")

        self._should_stop_cpu_utilization.set()

        self._cpu_utilizer_thread.join(timeout)
        if self._cpu_utilizer_thread.is_alive():
            logger.warning(
                "Timed out while waiting for CPU utilization thread to stop, "
                "it will be stopped forcefully when the parent process terminates"
            )
