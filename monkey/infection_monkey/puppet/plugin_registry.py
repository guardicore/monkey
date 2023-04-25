import logging
from copy import copy
from threading import RLock
from typing import Any, Dict

from serpentarium import PluginLoader, PluginThreadName, SingleUsePlugin

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginType
from common.event_queue import IAgentEventPublisher
from common.types import AgentID
from infection_monkey.exploit import IAgentBinaryRepository, IAgentOTPProvider
from infection_monkey.i_puppet import UnknownPluginError
from infection_monkey.island_api_client import IIslandAPIClient, IslandAPIRequestError
from infection_monkey.network import TCPPortSelector
from infection_monkey.propagation_credentials_repository import IPropagationCredentialsRepository

from . import PluginSourceExtractor
from infection_monkey.plugin.multiprocessing_plugin_wrapper import MultiprocessingPluginWrapper

logger = logging.getLogger()


# TODO: We should add an ExploiterPluginFactor and pass that to this component instead of passing
# all of the requirements for exploiters.
class PluginRegistry:
    def __init__(
        self,
        operating_system: OperatingSystem,
        island_api_client: IIslandAPIClient,
        plugin_source_extractor: PluginSourceExtractor,
        plugin_loader: PluginLoader,
        agent_binary_repository: IAgentBinaryRepository,
        agent_event_publisher: IAgentEventPublisher,
        propagation_credentials_repository: IPropagationCredentialsRepository,
        tcp_port_selector: TCPPortSelector,
        otp_provider: IAgentOTPProvider,
        agent_id: AgentID,
    ):
        """
        `self._registry` looks like -
            {
                AgentPluginType.EXPLOITER: {
                    "ZerologonExploiter": ZerologonExploiter,
                    "SMBExploiter": SMBExploiter
                }
            }
        """
        self._registry: Dict[AgentPluginType, Dict[str, SingleUsePlugin]] = {}

        self._operating_system = operating_system
        self._island_api_client = island_api_client
        self._plugin_source_extractor = plugin_source_extractor
        self._plugin_loader = plugin_loader
        self._agent_binary_repository = agent_binary_repository
        self._agent_event_publisher = agent_event_publisher
        self._propagation_credentials_repository = propagation_credentials_repository
        self._tcp_port_selector = tcp_port_selector
        self._otp_provider = otp_provider

        self._agent_id = agent_id
        self._lock = RLock()

    def get_plugin(self, plugin_type: AgentPluginType, plugin_name: str) -> Any:
        with self._lock:
            try:
                # Note: The MultiprocessingPluginWrapper is a MultiUsePlugin. The copy() used here
                # will be unnecessary once all functionality is encapsulated in plugins.
                return copy(self._registry[plugin_type][plugin_name])
            except KeyError:
                self._load_plugin_from_island(plugin_name, plugin_type)
                return copy(self._registry[plugin_type][plugin_name])

    def _load_plugin_from_island(self, plugin_name: str, plugin_type: AgentPluginType):
        agent_plugin = self._download_plugin_from_island(plugin_name, plugin_type)
        self._plugin_source_extractor.extract_plugin_source(agent_plugin)
        multiprocessing_plugin = MultiprocessingPluginWrapper(
            plugin_loader=self._plugin_loader,
            plugin_name=plugin_name,
            reset_modules_cache=False,
            main_thread_name=PluginThreadName.CALLING_THREAD,
            agent_id=self._agent_id,
            agent_binary_repository=self._agent_binary_repository,
            agent_event_publisher=self._agent_event_publisher,
            propagation_credentials_repository=self._propagation_credentials_repository,
            tcp_port_selector=self._tcp_port_selector,
            otp_provider=self._otp_provider,
        )

        self.load_plugin(plugin_type, plugin_name, multiprocessing_plugin)

    def _download_plugin_from_island(
        self, plugin_name: str, plugin_type: AgentPluginType
    ) -> AgentPlugin:
        try:
            plugin = self._island_api_client.get_agent_plugin(
                self._operating_system, plugin_type, plugin_name
            )
        except IslandAPIRequestError as err:
            raise UnknownPluginError(
                f"Unknown plugin '{plugin_name}' of type '{plugin_type.value}': {err}"
            )

        logger.debug(f"Plugin '{plugin_name}' downloaded from the island")
        return plugin

    def load_plugin(self, plugin_type: AgentPluginType, plugin_name: str, plugin: object) -> None:
        with self._lock:
            self._registry.setdefault(plugin_type, {})

        self._registry[plugin_type][plugin_name] = plugin
        logger.debug(f"Plugin '{plugin_name}' loaded")
