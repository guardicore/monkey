import logging
import threading

from common.event_queue import IAgentEventQueue
from common.tags import RESOURCE_HIJACKING_T1496_TAG
from common.types import AgentID, SocketAddress
from infection_monkey.utils.threading import create_daemon_thread

from .cryptojacker_options import CryptojackerOptions
from .typedef import (
    BitcoinMiningNetworkTrafficSimulatorCallable,
    CPUUtilizerCallable,
    MemoryUtilizerCallable,
)

logger = logging.getLogger(__name__)

CRYPTOJACKER_PAYLOAD_TAG = "cryptojacker-payload"
CRYPTOJACKER_TAGS = frozenset({CRYPTOJACKER_PAYLOAD_TAG, RESOURCE_HIJACKING_T1496_TAG})

THREAD_JOIN_TIMEOUT = 2  # seconds


class Cryptojacker:
    def __init__(
        self,
        options: CryptojackerOptions,
        utilize_cpu: CPUUtilizerCallable,
        utilize_memory: MemoryUtilizerCallable,
        simulate_bitcoin_mining_network_traffic: BitcoinMiningNetworkTrafficSimulatorCallable,
        agent_event_queue: IAgentEventQueue,
        agent_id: AgentID,
        island_server_address: SocketAddress,
    ):
        self._options = options
        self._utilize_cpu = utilize_cpu
        self._utilize_memory = utilize_memory
        self._simulate_bitcoin_mining_network_traffic = simulate_bitcoin_mining_network_traffic
        self._agent_event_queue = agent_event_queue
        self._agent_id = agent_id
        self._island_server_address = island_server_address

    def run(self, interrupt: threading.Event):
        cpu_utilization_thread = create_daemon_thread(
            target=self._utilize_cpu,
            name="CPUUtilizationThread",
            args=(interrupt),
        )

        memory_utilization_thread = create_daemon_thread(
            target=self._utilize_memory,
            name="MemoryUtilizationThread",
            args=(interrupt),
        )

        logger.info("Running cryptojacker payload")

        logger.info("Utilizing CPU")
        cpu_utilization_thread.start()

        logger.info("Utilizing memory")
        memory_utilization_thread.start()

        if self._options.simulate_bitcoin_mining_network_traffic:
            self._send_bitcoin_mining_network_traffic(interrupt)

        logger.info("Waiting for CPU utilization thread to stop")
        cpu_utilization_thread.join(THREAD_JOIN_TIMEOUT)
        if cpu_utilization_thread.is_alive():
            logger.info(
                "Timed out while waiting for CPU utilization thread to stop, forcefully killing it"
            )

        logger.info("Waiting for memory utilization thread to stop")
        memory_utilization_thread.join(THREAD_JOIN_TIMEOUT)
        if memory_utilization_thread.is_alive():
            logger.info(
                "Timed out while waiting for memory utilization thread to stop, "
                "forcefully killing it"
            )

    def _send_bitcoin_mining_network_traffic(self, interrupt: threading.Event):
        while True:  # TODO: Check simulation duration
            if interrupt.is_set():
                logger.debug("Received a stop signal, stopping Bitcoin mining network traffic")
                break

            try:
                logger.debug("Sending Bitcoin mining network traffic")

                self._simulate_bitcoin_mining_network_traffic(self._island_server_address)
                self._publish_some_event(success=True, error="")
            except Exception as err:
                logger.warning(f"Error sending Bitcoing mining network traffic: {err}")

                self._publish_some_event(success=False, error=str(err))

    # TODO: Replace with actual event
    def _publish_some_event(self, success: bool, error: str):
        class SomeEvent:
            pass

        some_event = SomeEvent(
            source=self._agent_id,
            success=success,
            error_message=error,
            tags=CRYPTOJACKER_TAGS,
        )
        self._agent_event_queue.publish(some_event)
