from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType


class IAgentPluginRepository(ABC):
    """A repository used to store `Agent` plugins"""

    @abstractmethod
    def get_plugin(
        self, host_operating_system: OperatingSystem, plugin_type: AgentPluginType, name: str
    ) -> AgentPlugin:
        """
        Retrieve AgentPlugin based on its name and type

        :param host_operating_system: The operating system the plugin runs on
        :param plugin_type: The type of the plugin
        :param name: The name of the plugin
        :raises RetrievalError: If an error occurs while attempting to retrieve the plugin
        :raises UnknownRecordError: If a plugin with specified name and type doesn't exist
        """
        pass

    @abstractmethod
    def get_all_plugin_configuration_schemas(
        self,
    ) -> Dict[AgentPluginType, Dict[str, Dict[str, Any]]]:
        """
        Retrieve the configuration schemas for all plugins.

        :raises RetrievalError: If an error occurs while trying to retrieve the configuration
            schemas
        """
        pass

    @abstractmethod
    def get_all_plugin_manifests(self) -> Dict[AgentPluginType, Dict[str, AgentPluginManifest]]:
        """
        Retrieve a collection of plugin manifests for all plugins.

        :raises RetrievalError: If an error occurs while trying to retrieve the manifests
        """
        pass

    @abstractmethod
    def store_agent_plugin(self, operating_system: OperatingSystem, agent_plugin: AgentPlugin):
        """
        Store AgentPlugin in the repository

        :param operating_system: The operating system the plugin runs on
        :param agent_plugin: The AgentPlugin object to be stored
        :raises StorageError: If the AgentPlugin could not be stored
        """

    @abstractmethod
    def remove_agent_plugin(
        self,
        agent_plugin_type: AgentPluginType,
        agent_plugin_name: str,
        operating_system: Optional[OperatingSystem] = None,
    ):
        """
        Remove AgentPlugin from repository

        :param agent_plugin_type: Type of the plugin we want to remove
        :param agent_plugin_name: Name of the plugin we want to remove
        :param operating_system: The operating system the plugin runs on
        :raises RemovalError: If an error occurs while removing the plugin
        """
