from monkey_island.cc.repositories import IAgentConfigurationRepository


class reset_agent_configuration:
    """
    Callable class that handles the reset of an agent configuration
    on the Island.
    """

    def __init__(
        self,
        agent_configuration_repository: IAgentConfigurationRepository,
    ):
        self._agent_configuration_repository = agent_configuration_repository

    def __call__(self):
        self._agent_configuration_repository.reset_to_default()
