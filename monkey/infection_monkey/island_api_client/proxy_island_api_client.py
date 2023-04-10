from multiprocessing.managers import BaseProxy  # , MakeProxyType
from typing import Any, Dict, Sequence

from common import AgentRegistrationData, AgentSignals, OperatingSystem
from common.agent_configuration import AgentConfiguration
from common.agent_events import AbstractAgentEvent
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType
from common.credentials import Credentials

from . import IIslandAPIClient

# ProxyHTTPIslandAPIClientBase = MakeProxyType("ProxyHTTPIslandAPIClientBase", IIslandAPIClient)


class ProxyIslandAPIClient(IIslandAPIClient, BaseProxy):
    """
    Proxy class for IslandAPIClient. Used to communicate with IslandAPIClient on a different process.

    Needs to be registered to a Manager using it's register method, e.g.: SyncManger.register('island_api_client', ProxyIslandAPIClient)

    Proxy types just forward calls to a remote object that is created by the manager.
    The remote object reference is stored in BaseProxy.
    """

    def login(self, otp: str):
        self._callmethod("login", (otp,))

    def logout(self):
        self._callmethod("logout", ())

    def get_agent_binary(self, operating_system: OperatingSystem) -> bytes:
        return self._callmethod("get_agent_binary", (operating_system,))

    def get_otp(self) -> str:
        return self._callmethod("get_otp", ())

    def get_agent_plugin(
        self, operating_system: OperatingSystem, plugin_type: AgentPluginType, plugin_name: str
    ) -> AgentPlugin:
        return self._callmethod("get_agent_plugin", (operating_system, plugin_type, plugin_name))

    def get_agent_plugin_manifest(
        self, plugin_type: AgentPluginType, plugin_name: str
    ) -> AgentPluginManifest:
        return self._callmethod("get_agent_plugin_manifest", (plugin_type, plugin_name))

    def get_agent_signals(self) -> AgentSignals:
        return self._callmethod("get_agent_signals", ())

    def get_agent_configuration_schema(self) -> Dict[str, Any]:
        return self._callmethod("get_agent_configuration_schema", ())

    def get_config(self) -> AgentConfiguration:
        return self._callmethod("get_config", ())

    def get_credentials_for_propagation(self) -> Sequence[Credentials]:
        return self._callmethod("get_credentials_for_propagation", ())

    def register_agent(self, agent_registration_data: AgentRegistrationData):
        return self._callmethod("register_agent", (agent_registration_data,))

    def send_events(self, events: Sequence[AbstractAgentEvent]):
        return self._callmethod("send_events", (events,))

    def send_heartbeat(self, timestamp: float):
        return self._callmethod("send_heartbeat", (timestamp,))

    def send_log(self, log_contents: str):
        return self._callmethod("send_log", (log_contents,))
