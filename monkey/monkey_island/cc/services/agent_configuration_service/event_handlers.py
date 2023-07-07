from . import IAgentConfigurationService


class reset_agent_configuration:
    """
    Callable class that handles the reset of an agent configuration
    on the Island.
    """

    def __init__(
        self,
        agent_configuration_service: IAgentConfigurationService,
    ):
        self._agent_configuration_service = agent_configuration_service

    def __call__(self):
        self._agent_configuration_service.reset_to_default()
