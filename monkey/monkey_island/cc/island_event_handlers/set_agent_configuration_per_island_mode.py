from common.agent_configuration import AgentConfiguration
from monkey_island.cc.models import IslandMode
from monkey_island.cc.repositories import IAgentConfigurationRepository


class set_agent_configuration_per_island_mode:
    """
    Callable class that sets the default Agent configuration as per the Island's mode
    """

    def __init__(
        self,
        agent_configuration_repository: IAgentConfigurationRepository,
        default_agent_configuration: AgentConfiguration,
        default_ransomware_agent_configuration: AgentConfiguration,
    ):
        self._agent_configuration_repository = agent_configuration_repository
        self._default_agent_configuration = default_agent_configuration
        self._default_ransomware_agent_configuration = default_ransomware_agent_configuration

    def __call__(self, mode: IslandMode):
        if mode == IslandMode.RANSOMWARE:
            self._agent_configuration_repository.update_configuration(
                self._default_ransomware_agent_configuration
            )
        else:
            self._agent_configuration_repository.update_configuration(
                self._default_agent_configuration
            )
