from typing import Any

from common.agent_configuration import AgentConfiguration
from monkey_island.cc.models import IslandMode
from monkey_island.cc.repository import IAgentConfigurationRepository


class set_island_mode:
    """
    Callable class that sets the Island's mode
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

    def __call__(self, event: Any = None):
        mode = event
        if mode == IslandMode.RANSOMWARE:
            self._agent_configuration_repository.store_configuration(
                self._default_ransomware_agent_configuration
            )
        else:
            self._agent_configuration_repository.store_configuration(
                self._default_agent_configuration
            )
