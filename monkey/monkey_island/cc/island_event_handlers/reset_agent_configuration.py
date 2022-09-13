from monkey_island.cc.repository import IAgentConfigurationRepository, IFileRepository


class reset_agent_configuration:
    """
    Callable class that handles removal of PBA files and reset of agent configuration
    on the Island.
    """

    def __init__(
        self,
        agent_configuration_repository: IAgentConfigurationRepository,
        file_repository: IFileRepository,
    ):
        self._agent_configuration_repository = agent_configuration_repository
        self._file_repository = file_repository

    def __call__(self):
        self._remove_pba_files()
        self._agent_configuration_repository.reset_to_default()

    def _remove_pba_files(self):
        """
        Removes PBA files from the file repository
        """
        agent_configuration = self._agent_configuration_repository.get_configuration()
        custom_pbas = agent_configuration.custom_pbas

        if custom_pbas.linux_filename:
            self._file_repository.delete_file(custom_pbas.linux_filename)

        if custom_pbas.windows_filename:
            self._file_repository.delete_file(custom_pbas.windows_filename)
