import logging

from egg_timer import EggTimer

from common.event_queue import IAgentEventQueue
from common.types import AgentID, Event, SocketAddress

from .bitcoin_mining_network_traffic_simulator import BitcoinMiningNetworkTrafficSimulator
from .cpu_utilizer import CPUUtilizer
from .cryptojacker_options import CryptojackerOptions
from .memory_utilizer import MemoryUtilizer

logger = logging.getLogger(__name__)

CRYPTOJACKER_PAYLOAD_TAG = "cryptojacker-payload"

COMPONENT_STOP_TIMEOUT = 30  # seconds
CHECK_DURATION_TIMER_INTERVAL = 5  # seconds


class Cryptojacker:
    def __init__(
        self,
        options: CryptojackerOptions,
        cpu_utilizer: CPUUtilizer,
        memory_utilizer: MemoryUtilizer,
        bitcoin_mining_network_traffic_simulator: BitcoinMiningNetworkTrafficSimulator,
        agent_id: AgentID,
        agent_event_queue: IAgentEventQueue,
        island_server_address: SocketAddress,
    ):
        self._options = options
        self._cpu_utilizer = cpu_utilizer
        self._memory_utilizer = memory_utilizer
        self._bitcoin_mining_network_traffic_simulator = bitcoin_mining_network_traffic_simulator
        self._agent_id = agent_id
        self._agent_event_queue = agent_event_queue
        self._island_server_address = island_server_address

    def run(self, interrupt: Event):
        logger.info("Running cryptojacker payload")

        timer = EggTimer()
        timer.set(self._options.duration)

        self._cpu_utilizer.start()
        self._memory_utilizer.start()
        if self._options.simulate_bitcoin_mining_network_traffic:
            self._bitcoin_mining_network_traffic_simulator.start()

        while not timer.is_expired() and not interrupt.is_set():
            interrupt.wait(CHECK_DURATION_TIMER_INTERVAL)

        logger.info("Stopping cryptojacker payload")

        self._cpu_utilizer.stop(timeout=COMPONENT_STOP_TIMEOUT)
        self._memory_utilizer.stop(timeout=COMPONENT_STOP_TIMEOUT)
        if self._options.simulate_bitcoin_mining_network_traffic:
            self._bitcoin_mining_network_traffic_simulator.stop(timeout=COMPONENT_STOP_TIMEOUT)
