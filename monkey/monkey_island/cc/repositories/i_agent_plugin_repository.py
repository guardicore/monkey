from abc import ABC, abstractmethod
from typing import Sequence, Tuple

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginType


class IAgentPluginRepository(ABC):
    """A repository used to store `Agent` plugins"""

    @abstractmethod
    def get_plugin(self, plugin_type: AgentPluginType, name: str) -> AgentPlugin:
        """
        Retrieve AgentPlugin based on its name and type

        :param plugin_type: The type of the plugin
        :param name: The name of the plugin
        :raises RetrievalError: If an error occurs while attempting to retrieve the plugin
        :raises UnknownRecordError: If a plugin with specified name and type doesn't exist
        """
        pass

    @abstractmethod
    def get_plugin_for_os(
        self, host_operating_system: OperatingSystem, plugin_type: AgentPluginType, name: str
    ) -> AgentPlugin:
        """
        Retrieve AgentPlugin based on its name and type, for a given operating system

        :param host_operating_system: The operating system on which the plugin will run
        :param plugin_type: The type of the plugin
        :param name: The name of the plugin
        :raises RetrievalError: If an error occurs while attempting to retrieve the plugin
        :raises UnknownRecordError: If a plugin with specified name and type doesn't exist
        """
        pass

    @abstractmethod
    def get_plugin_catalog(self) -> Sequence[Tuple[AgentPluginType, str, Tuple[OperatingSystem]]]:
        """
        Retrieve a sequence of agent plugin type, plugin name and supported operating systems.

        :raises RetrievalError: If an error occurs while attempting to retrieve the catalog
        """
