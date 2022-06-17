from abc import ABC

from common.configuration import AgentConfiguration


class IConfigRepository(ABC):
    """
    A repository used to store and retrieve the agent configuration.
    """

    def get_config(self) -> AgentConfiguration:
        """
        Retrieve the agent configuration from the repository

        :return: The agent configuration
        """
        pass

    def set_config(self, agent_config: AgentConfiguration):
        """
        Store the agent configuration in the repository

        :param agent_config: The agent configuration to store in the repository
        """
        pass
