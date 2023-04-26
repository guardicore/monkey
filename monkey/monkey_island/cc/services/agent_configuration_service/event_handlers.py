from common.agent_configuration import AgentConfiguration
from monkey_island.cc.models import IslandMode

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


class set_agent_configuration_per_island_mode:
    """
    Callable class that sets the default Agent configuration as per the Island's mode
    """

    def __init__(
        self,
        agent_configuration_service: IAgentConfigurationService,
        default_agent_configuration: AgentConfiguration,
        default_ransomware_agent_configuration: AgentConfiguration,
    ):
        self._agent_configuration_service = agent_configuration_service
        self._default_agent_configuration = default_agent_configuration
        self._default_ransomware_agent_configuration = default_ransomware_agent_configuration

    def __call__(self, mode: IslandMode):
        if mode == IslandMode.RANSOMWARE:
            self._agent_configuration_service.update_configuration(
                self._default_ransomware_agent_configuration
            )
        else:
            self._agent_configuration_service.update_configuration(
                self._default_agent_configuration
            )
