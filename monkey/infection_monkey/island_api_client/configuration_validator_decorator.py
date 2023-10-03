from typing import Any, Dict, Sequence

from jsonschema import validate
from monkeytypes import AgentPluginManifest, AgentPluginType

from common import AgentRegistrationData, AgentSignals, OperatingSystem
from common.agent_configuration import AgentConfiguration
from common.agent_events import AbstractAgentEvent
from common.agent_plugins import AgentPlugin
from common.credentials import Credentials

from . import IIslandAPIClient, IslandAPIError


class ConfigurationValidatorDecorator(IIslandAPIClient):
    """
    An IIslandAPIClient decorator that validates the agent configuration

    This decorator validates the agent configuration against the JSON Schema that includes plugin
    configurations. Since the AgentConfiguration class has no knowledge of valid or invalid plugin
    configurations, this decorator ensures that only valid configurations are returned to the
    caller.
    """

    def __init__(self, island_api_client: IIslandAPIClient):
        self._island_api_client = island_api_client

    def login(self, otp: str):
        return self._island_api_client.login(otp)

    def logout(self):
        return self._island_api_client.logout()

    def get_agent_binary(self, operating_system: OperatingSystem) -> bytes:
        return self._island_api_client.get_agent_binary(operating_system)

    def get_otp(self) -> str:
        return self._island_api_client.get_otp()

    def get_agent_plugin(
        self, operating_system: OperatingSystem, plugin_type: AgentPluginType, plugin_name: str
    ) -> AgentPlugin:
        return self._island_api_client.get_agent_plugin(operating_system, plugin_type, plugin_name)

    def get_agent_plugin_manifest(
        self,
        plugin_type: AgentPluginType,
        plugin_name: str,
    ) -> AgentPluginManifest:
        return self._island_api_client.get_agent_plugin_manifest(plugin_type, plugin_name)

    def get_agent_signals(self) -> AgentSignals:
        return self._island_api_client.get_agent_signals()

    def get_agent_configuration_schema(self) -> Dict[str, Any]:
        return self._island_api_client.get_agent_configuration_schema()

    def get_config(self) -> AgentConfiguration:
        try:
            agent_configuration = self._island_api_client.get_config()
            agent_configuration_schema = self._island_api_client.get_agent_configuration_schema()
            validate(
                instance=agent_configuration.dict(simplify=True), schema=agent_configuration_schema
            )
            return agent_configuration
        except Exception as err:
            raise IslandAPIError(f"Invalid agent configuration: {err}")

    def get_credentials_for_propagation(self) -> Sequence[Credentials]:
        return self._island_api_client.get_credentials_for_propagation()

    def register_agent(self, agent_registration_data: AgentRegistrationData):
        return self._island_api_client.register_agent(agent_registration_data)

    def send_events(self, events: Sequence[AbstractAgentEvent]):
        return self._island_api_client.send_events(events)

    def send_heartbeat(self, timestamp: float):
        return self._island_api_client.send_heartbeat(timestamp)

    def send_log(self, log_contents: str):
        return self._island_api_client.send_log(log_contents)

    def terminate_signal_is_set(self) -> bool:
        return self._island_api_client.terminate_signal_is_set()
