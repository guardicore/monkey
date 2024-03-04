import logging
from pprint import pformat

from agentpluginapi import IAgentEventPublisher
from monkeytypes import AgentID, OperatingSystem, PercentLimited, SocketAddress

from .bitcoin_mining_network_traffic_simulator import BitcoinMiningNetworkTrafficSimulator
from .cpu_utilizer import CPUUtilizer
from .cryptojacker import Cryptojacker
from .cryptojacker_options import CryptojackerOptions
from .memory_utilizer import MemoryUtilizer

logger = logging.getLogger(__name__)


def build_cryptojacker(
    options: CryptojackerOptions,
    agent_id: AgentID,
    agent_event_publisher: IAgentEventPublisher,
    island_server_address: SocketAddress,
    operating_system: OperatingSystem,
):
    logger.debug(f"Cryptojacker configuration:\n{pformat(options)}")

    cpu_utilizer = _build_cpu_utilizer(
        options.cpu_utilization,
        agent_id,
        agent_event_publisher,
        operating_system,
    )
    memory_utilizer = _build_memory_utilizer(
        options.memory_utilization, agent_id, agent_event_publisher
    )
    bitcoin_mining_network_traffic_simulator = _build_bitcoin_mining_network_traffic_simulator(
        island_server_address, agent_id, agent_event_publisher
    )

    return Cryptojacker(
        options=options,
        cpu_utilizer=cpu_utilizer,
        memory_utilizer=memory_utilizer,
        bitcoin_mining_network_traffic_simulator=bitcoin_mining_network_traffic_simulator,
    )


def _build_cpu_utilizer(
    cpu_utilization: PercentLimited,
    agent_id: AgentID,
    agent_event_publisher: IAgentEventPublisher,
    operating_system: OperatingSystem,
) -> CPUUtilizer:
    return CPUUtilizer(cpu_utilization, agent_id, agent_event_publisher, operating_system)


def _build_memory_utilizer(
    memory_utilization: PercentLimited,
    agent_id: AgentID,
    agent_event_publisher: IAgentEventPublisher,
) -> MemoryUtilizer:
    return MemoryUtilizer(memory_utilization, agent_id, agent_event_publisher)


def _build_bitcoin_mining_network_traffic_simulator(
    island_server_address: SocketAddress,
    agent_id: AgentID,
    agent_event_publisher: IAgentEventPublisher,
) -> BitcoinMiningNetworkTrafficSimulator:
    return BitcoinMiningNetworkTrafficSimulator(
        island_server_address, agent_id, agent_event_publisher
    )
