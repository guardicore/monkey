from abc import ABC, abstractmethod

from serpentarium import SingleUsePlugin


class IPluginFactory(ABC):
    """
    Abstract base class for factories that create plugins for specific `AgentPluginType`s
    """

    @abstractmethod
    def create(self, plugin_name: str) -> SingleUsePlugin:
        """
        Create a plugin with the given name

        :param plugin_name: The name of the plugin to create
        :return: A plugin with the given name
        """
        pass
