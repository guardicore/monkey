from abc import ABC, abstractmethod
from typing import Any, Dict

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType


class IAgentPluginService(ABC):
    """
    A service for retrieving and manipulating Agent plugins
    """

    @abstractmethod
    def get_plugin(
        self, host_operating_system: OperatingSystem, plugin_type: AgentPluginType, name: str
    ) -> AgentPlugin:
        """
        Retrieve AgentPlugin based on its name and type

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
        Retrieve the configuration schemas for all plugins

        :raises RetrievalError: If an error occurs while trying to retrieve the configuration
                                schemas
        """
        pass

    @abstractmethod
    def get_all_plugin_manifests(self) -> Dict[AgentPluginType, Dict[str, AgentPluginManifest]]:
        """
        Retrieve a sequence of plugin manifests for all plugins

        :raises RetrievalError: If an error occurs while trying to retrieve the manifests
        """
        pass

    @abstractmethod
    def install_agent_plugin_archive(self, agent_plugin_archive: bytes):
        """
        Install plugin archive

        :param agent_plugin_archive: The archive of the plugin
        :raises RemovalError: If an error occus while attempting to uninstall a previous
        version of the plugin
        :raises StorageError: If an error occurs while attempting to install the plugin
        """
        pass
