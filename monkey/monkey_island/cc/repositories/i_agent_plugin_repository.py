from abc import ABC, abstractmethod

from common.agent_plugins import AgentPlugin, AgentPluginType


class IAgentPluginRepository(ABC):
    """A repository used to store `Agent` plugins"""

    @abstractmethod
    def get_plugin(self, name: str, plugin_type: AgentPluginType) -> AgentPlugin:
        """
        Retrieve AgentPlugin based on it's name and type


        :param name: The name of the plugin
        :param plugin_type: The type of the plugin
        :raises RetrievalError: If an error occurs while attempting to retrieve the plugin
        :raises UnknownRecordError: If a plugin with specified name and type doesn't
         exist in the repository
        """
        pass
