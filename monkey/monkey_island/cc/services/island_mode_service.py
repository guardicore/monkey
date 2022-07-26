from common.agent_configuration import AgentConfiguration
from monkey_island.cc.models import IslandMode
from monkey_island.cc.repository import IAgentConfigurationRepository, ISimulationRepository


class IslandModeService:
    def __init__(
        self,
        _agent_configuration_repository: IAgentConfigurationRepository,
        simulation_repository: ISimulationRepository,
        default_agent_configuration: AgentConfiguration,
        default_ransomware_agent_configuration: AgentConfiguration,
    ):
        self._agent_configuration_repository = _agent_configuration_repository
        self._simulation_repository = simulation_repository
        self._default_agent_configuration = default_agent_configuration
        self._default_ransomware_agent_configuration = default_ransomware_agent_configuration

    def get_mode(self):
        """
        Get's the island's current mode

        :return The island's current mode
        :raises RetrievalError: If the mode could not be retrieved
        """
        return self._simulation_repository.get_mode()

    def set_mode(self, mode: IslandMode):
        """
        Set the island's mode

        :param mode: The island's new mode
        :raises StorageError: If the mode could not be saved
        """
        self._simulation_repository.set_mode(mode)
        self._set_configuration(mode)

    def _set_configuration(self, mode: IslandMode):
        if mode == IslandMode.RANSOMWARE:
            self._agent_configuration_repository.store_configuration(
                self._default_ransomware_agent_configuration
            )
        else:
            self._agent_configuration_repository.store_configuration(
                self._default_agent_configuration
            )
