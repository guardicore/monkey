import logging
import time

from egg_timer import EggTimer

from common.event_queue import IAgentEventQueue
from common.tags import RESOURCE_HIJACKING_T1496_TAG
from common.types import AgentID, Event, SocketAddress
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
CHECK_DURATION_TIMER_INTERVAL = 5  # seconds


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

    def run(self, interrupt: Event):
        should_utilize_cpu = Event()
        cpu_utilization_thread = create_daemon_thread(
            target=self._utilize_cpu,
            name="CPUUtilizationThread",
            args=(should_utilize_cpu),
        )

        should_utilize_memory = Event()
        memory_utilization_thread = create_daemon_thread(
            target=self._utilize_memory,
            name="MemoryUtilizationThread",
            args=(should_utilize_memory),
        )

        should_send_bitcoin_mining_network_traffic = Event()
        bitcoin_mining_network_traffic_thread = create_daemon_thread(
            target=self._send_bitcoin_mining_network_traffic,
            name="BitcoinMiningNetworkTrafficThread",
            args=(should_send_bitcoin_mining_network_traffic),
        )

        logger.info("Running cryptojacker payload")

        timer = EggTimer()
        timer.set(self._options.duration)

        logger.info("Utilizing CPU")
        cpu_utilization_thread.start()

        logger.info("Utilizing memory")
        memory_utilization_thread.start()

        if self._options.simulate_bitcoin_mining_network_traffic:
            logger.info("Sending Bitcoin mining network traffic")
            bitcoin_mining_network_traffic_thread.start()

        while not timer.is_expired() and not interrupt.is_set():
            time.sleep(CHECK_DURATION_TIMER_INTERVAL)

        if bitcoin_mining_network_traffic_thread.is_alive():
            logger.info("Stopping Bitcoin mining network traffic")
            should_send_bitcoin_mining_network_traffic.set()
            bitcoin_mining_network_traffic_thread.join(THREAD_JOIN_TIMEOUT)
            if bitcoin_mining_network_traffic_thread.is_alive():
                logger.info(
                    "Timed out while waiting for Bitcoin mining network traffic thread to stop, "
                    "it will be stopped forcefully when the parent process terminates"
                )

        logger.info("Stopping CPU utilization")
        should_utilize_cpu.set()
        cpu_utilization_thread.join(THREAD_JOIN_TIMEOUT)
        if cpu_utilization_thread.is_alive():
            logger.info(
                "Timed out while waiting for CPU utilization thread to stop, "
                "it will be stopped forcefully when the parent process terminates"
            )

        logger.info("Stopping memory utilization")
        should_utilize_memory.set()
        memory_utilization_thread.join(THREAD_JOIN_TIMEOUT)
        if memory_utilization_thread.is_alive():
            logger.info(
                "Timed out while waiting for memory utilization thread to stop, "
                "it will be stopped forcefully when the parent process terminates"
            )

    def _send_bitcoin_mining_network_traffic(
        self, should_send_bitcoin_mining_network_traffic: Event
    ):
        while not should_send_bitcoin_mining_network_traffic.is_set():
            self._simulate_bitcoin_mining_network_traffic(self._island_server_address)
