from typing import Any, Dict, Sequence

from monkeytypes import AgentPluginManifest, AgentPluginType

from common import AgentRegistrationData, AgentSignals, OperatingSystem
from common.agent_configuration import AgentConfiguration
from common.agent_events import AbstractAgentEvent
from common.agent_plugins import AgentPlugin
from common.credentials import Credentials
from infection_monkey.island_api_client import IIslandAPIClient


class BaseIslandAPIClient(IIslandAPIClient):
    def login(self, otp: str):
        return

    def logout(self):
        return

    def get_agent_binary(self, operating_system: OperatingSystem) -> bytes:
        return b""

    def get_agent_plugin(
        self, operating_system: OperatingSystem, plugin_type: AgentPluginType, plugin_name: str
    ) -> AgentPlugin:
        return AgentPlugin()

    def get_otp(self):
        return

    def get_agent_plugin_manifest(
        self, plugin_type: AgentPluginType, plugin_name: str
    ) -> AgentPluginManifest:
        return AgentPluginManifest()

    def get_agent_signals(self) -> AgentSignals:
        return AgentSignals()

    def get_agent_configuration_schema(self) -> Dict[str, Any]:
        return {}

    def get_config(self) -> AgentConfiguration:
        return AgentConfiguration()

    def get_credentials_for_propagation(self) -> Sequence[Credentials]:
        return []

    def register_agent(self, agent_registration_data: AgentRegistrationData):
        return

    def send_events(self, events: Sequence[AbstractAgentEvent]):
        return

    def send_heartbeat(self, timestamp: float):
        return

    def send_log(self, log_contents: str):
        return

    def terminate_signal_is_set(self) -> bool:
        return True
