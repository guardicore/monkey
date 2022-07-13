from monkey_island.cc.repository import IAgentConfigurationRepository, IFileRepository


class RepositoryService:
    def __init__(
        self,
        agent_configuration_repository: IAgentConfigurationRepository,
        file_repository: IFileRepository,
    ):
        self._agent_configuration_repository = agent_configuration_repository
        self._file_repository = file_repository

    def reset_agent_configuration(self):
        # NOTE: This method will be replaced by an event when we implement pub/sub in the island.
        #       Different plugins and components will be able to register for the event and reset
        #       their configurations.
        self._remove_pba_files()
        self._agent_configuration_repository.reset_to_default()

    def _remove_pba_files(self):
        agent_configuration = self._agent_configuration_repository.get_configuration()
        custom_pbas = agent_configuration.custom_pbas

        if custom_pbas.linux_filename:
            self._file_repository.delete_file(custom_pbas.linux_filename)

        if custom_pbas.windows_filename:
            self._file_repository.delete_file(custom_pbas.windows_filename)

    def unlock(self):
        raise NotImplementedError

    def reset_key(self):
        raise NotImplementedError

    def clear_simulation_data(self):
        # NOTE: This method will be replaced by an event when we implement pub/sub in the island.
        #       Different plugins and components will be able to register for the event and clear
        #       any configuration data they've collected.
        raise NotImplementedError
