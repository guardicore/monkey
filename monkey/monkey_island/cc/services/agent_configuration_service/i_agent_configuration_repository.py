from abc import ABC, abstractmethod

from common.agent_configuration import AgentConfiguration
from monkey_island.cc.repositories import RepositoryError


class PluginConfigurationValidationError(RepositoryError):
    """
    Raised when invalid plugin configuration is encountered
    """


class IAgentConfigurationRepository(ABC):
    """
    A repository used to store and retrieve the agent configuration.
    """

    @abstractmethod
    def get_configuration(self) -> AgentConfiguration:
        """
        Retrieve the agent configuration from the repository

        :return: The agent configuration as retrieved from the repository, or the default
                 configuration if the repository is empty
        :raises RetrievalError: If the configuration could not be retrieved
        """
        pass

    @abstractmethod
    def update_configuration(self, agent_configuration: AgentConfiguration):
        """
        Update the agent configuration in the repository

        :param agent_configuration: The new agent configuration to store in the repository
        :raises PluginConfigurationValidationError: If the new agent configuration has an invalid
                configuration for any plugin
        :raises StorageError: If the configuration could not be updated
        """
        pass

    @abstractmethod
    def reset_to_default(self):
        """
        Reset the repository's configuration to the default values

        :raises RemovalError: If the repository could not be reset
        """
        pass
