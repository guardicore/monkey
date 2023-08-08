import logging
from pprint import pformat

from common.event_queue import IAgentEventQueue
from common.types import AgentID, PercentLimited, SocketAddress

from .bitcoin_mining_network_traffic_simulator import BitcoinMiningNetworkTrafficSimulator
from .cpu_utilizer import CPUUtilizer
from .cryptojacker import Cryptojacker
from .cryptojacker_options import CryptojackerOptions
from .memory_utilizer import MemoryUtilizer

logger = logging.getLogger(__name__)


def build_cryptojacker(
    options: CryptojackerOptions,
    agent_id: AgentID,
    agent_event_queue: IAgentEventQueue,
    island_server_address: SocketAddress,
):
    logger.debug(f"Cryptojacker configuration:\n{pformat(options)}")

    cpu_utilizer = _build_cpu_utilizer(options.cpu_utilization)
    memory_utilizer = _build_memory_utilizer(options.memory_utilization)
    bitcoin_mining_network_traffic_simulator = _build_bitcoin_mining_network_traffic_simulator()

    return Cryptojacker(
        options=options,
        utilize_cpu=cpu_utilizer,
        utilize_memory=memory_utilizer,
        simulate_bitcoin_mining_network_traffic=bitcoin_mining_network_traffic_simulator,
        agent_id=agent_id,
        agent_event_queue=agent_event_queue,
        island_server_address=island_server_address,
    )


def _build_cpu_utilizer(cpu_utilization: PercentLimited):
    return CPUUtilizer(cpu_utilization)


def _build_memory_utilizer(memory_utilization: PercentLimited):
    return MemoryUtilizer(memory_utilization)


def _build_bitcoin_mining_network_traffic_simulator():
    return BitcoinMiningNetworkTrafficSimulator()
