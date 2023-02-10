from typing import Any, Dict, Sequence

from common import AgentRegistrationData, AgentSignals, OperatingSystem
from common.agent_configuration import AgentConfiguration
from common.agent_events import AbstractAgentEvent
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType
from common.credentials import Credentials
from common.types import AgentID, SocketAddress
from infection_monkey.island_api_client import IIslandAPIClient


class BaseIslandAPIClient(IIslandAPIClient):
    def connect(self, island_server: SocketAddress):
        pass

    def get_agent_binary(self, operating_system: OperatingSystem) -> bytes:
        pass

    def get_agent_plugin(self, plugin_type: AgentPluginType, plugin_name: str) -> AgentPlugin:
        pass

    def get_agent_plugin_manifest(
        self, plugin_type: AgentPluginType, plugin_name: str
    ) -> AgentPluginManifest:
        pass

    def get_agent_signals(self, agent_id: str) -> AgentSignals:
        pass

    def get_agent_configuration_schema(self) -> Dict[str, Any]:
        pass

    def get_config(self) -> AgentConfiguration:
        pass

    def get_credentials_for_propagation(self) -> Sequence[Credentials]:
        pass

    def register_agent(self, agent_registration_data: AgentRegistrationData):
        pass

    def send_events(self, events: Sequence[AbstractAgentEvent]):
        pass

    def send_heartbeat(self, agent: AgentID, timestamp: float):
        pass

    def send_log(self, agent_id: AgentID, log_contents: str):
        pass
