from typing import Optional

from common.event_queue import IAgentEventPublisher
from common.types import AgentID, SocketAddress


class BitcoinMiningNetworkTrafficSimulator:
    def __init__(
        self,
        island_server_address: SocketAddress,
        agent_id: AgentID,
        agent_event_publisher: IAgentEventPublisher,
    ):
        self._island_server_address = island_server_address
        self._agent_id = agent_id
        self._agent_event_publisher = agent_event_publisher

    def start(self):
        pass

    def stop(self, timeout: Optional[float] = None):
        pass
