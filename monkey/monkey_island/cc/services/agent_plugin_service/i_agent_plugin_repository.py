from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from monkeytypes import AgentPluginManifest, AgentPluginType

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, PluginName


class IAgentPluginRepository(ABC):
    """A repository used to store `Agent` plugins"""

    @abstractmethod
    def get_plugin(
        self, host_operating_system: OperatingSystem, plugin_type: AgentPluginType, name: PluginName
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
    ) -> Dict[AgentPluginType, Dict[PluginName, Dict[str, Any]]]:
        """
        Retrieve the configuration schemas for all plugins.

        :raises RetrievalError: If an error occurs while trying to retrieve the configuration
            schemas
        """
        pass

    @abstractmethod
    def get_all_plugin_manifests(
        self,
    ) -> Dict[AgentPluginType, Dict[PluginName, AgentPluginManifest]]:
        """
        Retrieve a collection of plugin manifests for all plugins.

        :raises RetrievalError: If an error occurs while trying to retrieve the manifests
        """
        pass

    # NOTE: There's a theoretical architectural flaw in this interface. The issue stems from the
    #       fact that there are effectively two types of plugin objects and we're using one class to
    #       represent both. A plugin packaged for distribution (hereafter called a "distribution
    #       plugin") contains the Windows and Linux files needed for the plugin to run whichever OS
    #       is desired. These distribution plugins get parsed into OS-specific plugins (hereafter
    #       referred to as "runnables").
    #
    #       This interface is confusing because it provides config schemas and manifests for
    #       distributions, but plugins are stored as runnables, not distributions. In practice, this
    #       isn't an issue at the present time. However, as a matter of cleanliness, it would be
    #       nice to refactor this to provide a better interface.
    #
    #       The proposed solution is to split this into two Repository interfaces: one for storing
    #       distribution plugins and one for storing runnables. The distribution plugin repository
    #       can provide get_all_plugin_{config_schemas,manifests} methods, while the runnable plugin
    #       repository can provide {get,store}_plugin methods.
    @abstractmethod
    def store_agent_plugin(self, operating_system: OperatingSystem, agent_plugin: AgentPlugin):
        """
        Store AgentPlugin in the repository

        If the the repository already contains the plugin for the given operating system, it will
        be overwritten.

        :param operating_system: The operating system the plugin runs on
        :param agent_plugin: The AgentPlugin object to be stored
        :raises StorageError: If the AgentPlugin could not be stored
        """

    @abstractmethod
    def remove_agent_plugin(
        self,
        agent_plugin_type: AgentPluginType,
        agent_plugin_name: PluginName,
        operating_system: Optional[OperatingSystem] = None,
    ):
        """
        Remove AgentPlugin from repository

        :param agent_plugin_type: Type of the plugin we want to remove
        :param agent_plugin_name: Name of the plugin we want to remove
        :param operating_system: The operating system the plugin runs on
        :raises RemovalError: If an error occurs while removing the plugin
        """
