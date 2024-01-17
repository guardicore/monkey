from typing import Callable

from agentpluginapi import LocalMachineInfo
from monkeytypes import AgentID, SocketAddress
from serpentarium import SingleUsePlugin

from common.event_queue import IAgentEventPublisher

from .i_plugin_factory import IPluginFactory


class PayloadPluginFactory(IPluginFactory):
    def __init__(
        self,
        agent_id: AgentID,
        agent_event_publisher: IAgentEventPublisher,
        island_server_address: SocketAddress,
        local_machine_info: LocalMachineInfo,
        create_plugin: Callable[..., SingleUsePlugin],
    ):
        self._agent_id = agent_id
        self._island_server_address = island_server_address
        self._agent_event_publisher = agent_event_publisher
        self._local_machine_info = local_machine_info
        self._create_plugin = create_plugin

    def create(self, plugin_name: str) -> SingleUsePlugin:
        return self._create_plugin(
            plugin_name=plugin_name,
            agent_id=self._agent_id,
            agent_event_publisher=self._agent_event_publisher,
            island_server_address=self._island_server_address,
            local_machine_info=self._local_machine_info,
        )
