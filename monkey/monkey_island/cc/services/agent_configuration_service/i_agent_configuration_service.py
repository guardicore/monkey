from abc import ABC, abstractmethod

from common.agent_configuration import AgentConfiguration


class IAgentConfigurationService(ABC):
    """
    A service for storing and retrieving the agent configuration.
    """

    @abstractmethod
    def get_schema(self):
        """
        Get the Agent configuration schema

        :return: Agent configuration schema
        :raises RuntimeError: If the schema could not be retrieved
        """
        pass

    @abstractmethod
    def get_configuration(self) -> AgentConfiguration:
        """
        Retrieve the agent configuration

        :return: The currently stored agent configuration, or the default
                 configuration if no configuration has yet been stored
        :raises RetrievalError: If the configuration could not be retrieved
        """
        pass

    @abstractmethod
    def update_configuration(self, agent_configuration: AgentConfiguration):
        """
        Update the agent configuration

        :param agent_configuration: The new agent configuration
        :raises PluginConfigurationValidationError: If the new agent configuration has an invalid
                configuration for any plugin
        :raises StorageError: If the configuration could not be updated
        """
        pass

    @abstractmethod
    def reset_to_default(self):
        """
        Reset the configuration to the default values

        :raises RemovalError: If the configuration could not be reset
        """
        pass
