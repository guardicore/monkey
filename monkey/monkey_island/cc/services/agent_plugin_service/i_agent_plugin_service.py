from abc import ABC, abstractmethod
from typing import Any, Dict

from monkeytypes import AgentPluginType

from common import OperatingSystem
from common.agent_plugins import (
    AgentPlugin,
    AgentPluginManifest,
    AgentPluginRepositoryIndex,
    PluginName,
    PluginVersion,
)


class IAgentPluginService(ABC):
    """
    A service for retrieving and manipulating Agent plugins
    """

    @abstractmethod
    def get_plugin(
        self,
        host_operating_system: OperatingSystem,
        plugin_type: AgentPluginType,
        plugin_name: PluginName,
    ) -> AgentPlugin:
        """
        Retrieve AgentPlugin based on its name and type

        :param plugin_type: The type of the plugin
        :param plugin_name: The name of the plugin
        :raises RetrievalError: If an error occurs while attempting to retrieve the plugin
        :raises UnknownRecordError: If a plugin with specified name and type doesn't exist
        """
        pass

    @abstractmethod
    def get_all_plugin_configuration_schemas(
        self,
    ) -> Dict[AgentPluginType, Dict[PluginName, Dict[str, Any]]]:
        """
        Retrieve the configuration schemas for all plugins

        :raises RetrievalError: If an error occurs while trying to retrieve the configuration
                                schemas
        """
        pass

    @abstractmethod
    def get_all_plugin_manifests(
        self,
    ) -> Dict[AgentPluginType, Dict[PluginName, AgentPluginManifest]]:
        """
        Retrieve a sequence of plugin manifests for all plugins

        :raises RetrievalError: If an error occurs while trying to retrieve the manifests
        """
        pass

    @abstractmethod
    def install_plugin_archive(self, agent_plugin_archive: bytes):
        """
        Install plugin archive

        :param agent_plugin_archive: The archive of the plugin
        :raises RemovalError: If an error occurs while attempting to uninstall a previous
                              version of the plugin
        :raises StorageError: If an error occurs while attempting to store the plugin
        :raises PluginInstallationError: If an error occurs while attempting to install the plugin
        """
        pass

    @abstractmethod
    def install_plugin_from_repository(
        self, plugin_type: AgentPluginType, plugin_name: PluginName, plugin_version: PluginVersion
    ):
        """
        Install plugin from repository

        :param plugin_type: The type of the plugin
        :param plugin_name: The name of the plugin
        :param plugin_version: The version of the plugin
        :raises RemovalError: If an error occurs while attempting to uninstall a previous
                              version of the plugin
        :raises StorageError: If an error occurs while attempting to store the plugin
        :raises PluginInstallationError: If an error occurs while attempting to install the plugin
        """

    @abstractmethod
    def get_available_plugins(self, force_refresh: bool) -> AgentPluginRepositoryIndex:
        """
        Retrieve plugin repository index for all available plugins in a repository

        Returns a cached result unless it has expired or force_refresh is `True`

        :param force_refresh: If true, ignores the cached result and requests the index from
                              the repository again
        :raises RetrievalError: If an error occurs while attempting to get the index of all
                                available plugins from the repository
        """
        pass

    @abstractmethod
    def uninstall_plugin(self, plugin_type: AgentPluginType, plugin_name: PluginName):
        """
        Uninstall agent plugin

        :param plugin_type: The type of the plugin
        :param plugin_name: The name of the plugin
        :raises PluginUninstallationError: If an error occurs while uninstalling the plugin
        """
        pass
