import logging
import time
from typing import Optional

import psutil

from common.agent_events import RAMConsumptionEvent
from common.event_queue import IAgentEventPublisher
from common.tags import RESOURCE_HIJACKING_T1496_TAG
from common.types import AgentID, PercentLimited
from common.utils.code_utils import PeriodicCaller

from .consts import CRYPTOJACKER_PAYLOAD_TAG

MEMORY_CONSUMPTION_CHECK_INTERVAL = 30
# If target memory consumption is within 2% of actual consumption, we'll consider it close enough.
MEMORY_CONSUMPTION_NOP_THRESHOLD = 0.02
# We don't want to ever use more then 90% of available memory, otherwise we risk impacting the
# victim machines performance
MEMORY_CONSUMPTION_SAFETY_LIMIT = 0.9

logger = logging.getLogger(__name__)


class MemoryUtilizer:
    def __init__(
        self,
        target_utilization: PercentLimited,
        agent_id: AgentID,
        agent_event_publisher: IAgentEventPublisher,
    ):
        self._agent_id = agent_id
        self._agent_event_publisher = agent_event_publisher
        self._target_utilization = target_utilization
        self._consumed_bytes = b""

        self._periodic_caller = PeriodicCaller(
            self.adjust_memory_utilization,
            MEMORY_CONSUMPTION_CHECK_INTERVAL,
            name="Cryptojacker.MemoryUtilizer",
        )

    @property
    def consumed_bytes_size(self) -> int:
        try:
            return len(self._consumed_bytes)
        except AttributeError:
            # self._consumed_bytes was deleted and is currently being reinitialized return 0 while
            # we wait.
            return 0

    def start(self):
        logger.debug("Starting MemoryUtilizer")
        self._periodic_caller.start()

    def adjust_memory_utilization(self):
        try:
            memory_to_consume = self._calculate_memory_to_consume()
            self.consume_bytes(len(self._consumed_bytes) + memory_to_consume)
        except RuntimeError as err:
            logger.error("Failed to adjust memory utilization: %s", err)

    def _calculate_memory_to_consume(self) -> int:
        total_virtual_memory = psutil.virtual_memory().total
        available_virtual_memory = psutil.virtual_memory().available
        used_virtual_memory = psutil.Process().memory_info().vms

        if used_virtual_memory > total_virtual_memory:
            raise RuntimeError("Impossible system state: Used memory is greater than total memory")

        ideal_memory_to_consume = int(
            total_virtual_memory * self._target_utilization.as_decimal_fraction()
            - used_virtual_memory
        )
        maximum_memory_to_consume = int(
            (available_virtual_memory + used_virtual_memory) * MEMORY_CONSUMPTION_SAFETY_LIMIT
            - used_virtual_memory
        )

        # We never want to consume 100% of available memory, otherwise the OS could kill this
        # process or one of the user's mission-critical processes. This logic limits the amount of
        # memory we consume to 90% of available memory.
        return min(ideal_memory_to_consume, maximum_memory_to_consume)

    def consume_bytes(self, bytes_: int):
        logger.debug(
            f"Currently consumed: {self.consumed_bytes_size} bytes - Target: {bytes_} bytes"
        )

        if not self._should_change_byte_consumption(bytes_):
            logger.debug("Not adjusting memory consumption, as the difference is too small")
            return

        timestamp = time.time()
        if bytes_ <= 0:
            self._consumed_bytes = bytearray(0)
        else:
            # If len(self._consumed_bytes) > 50% of available RAM, we must delete it before
            # reassigning it to a new bytearray. Otherwise, the new bytearray may be allocated to
            # more than 50% of total RAM before the original byte array is garbage collected.
            # This will cause this process to consume all available ram until the OS to kills this
            # process or an out-of-memory error occurs.
            del self._consumed_bytes
            self._consumed_bytes = bytearray(bytes_)

        self._publish_ram_consumption_event(timestamp)

    def _should_change_byte_consumption(self, target_consumption_bytes_: int) -> bool:
        if target_consumption_bytes_ <= 0:
            if self.consumed_bytes_size == 0:
                return False

            return True

        percent_difference = (
            abs(self.consumed_bytes_size - target_consumption_bytes_) / target_consumption_bytes_
        )
        if percent_difference <= MEMORY_CONSUMPTION_NOP_THRESHOLD:
            return False

        return True

    def _publish_ram_consumption_event(self, timestamp: float):
        total_virtual_memory = psutil.virtual_memory().total
        used_virtual_memory = psutil.Process().memory_info().vms

        self._agent_event_publisher.publish(
            RAMConsumptionEvent(
                source=self._agent_id,
                timestamp=timestamp,
                bytes=used_virtual_memory,
                utilization=(used_virtual_memory / total_virtual_memory) * 100,
                tags=frozenset({CRYPTOJACKER_PAYLOAD_TAG, RESOURCE_HIJACKING_T1496_TAG}),
            )
        )

    def stop(self, timeout: Optional[float] = None):
        logger.debug("Stopping MemoryUtilizer")
        self._periodic_caller.stop(timeout=timeout)
