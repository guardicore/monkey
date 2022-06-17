from abc import ABC

from common.configuration import AgentConfiguration


class IConfigurationRepository(ABC):
    """
    A repository used to store and retrieve the agent configuration.
    """

    def get_configuration(self) -> AgentConfiguration:
        """
        Retrieve the agent configuration from the repository

        :return: The agent configuration
        """
        pass

    def set_configuration(self, agent_configuration: AgentConfiguration):
        """
        Store the agent configuration in the repository

        :param agent_configuration: The agent configuration to store in the repository
        """
        pass
