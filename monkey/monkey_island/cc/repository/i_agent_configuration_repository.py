from abc import ABC, abstractmethod

from common.agent_configuration import AgentConfiguration


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
    def store_configuration(self, agent_configuration: AgentConfiguration):
        """
        Store the agent configuration in the repository

        :param agent_configuration: The agent configuration to store in the repository
        :raises StorageError: If the configuration could not be stored
        """
        pass

    @abstractmethod
    def reset_to_default(self):
        """
        Remove any stored configuration from the repository

        :raises RemovalError: If the repository could not be reset
        """
        pass
