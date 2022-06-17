import io

from common.configuration import (
    DEFAULT_AGENT_CONFIGURATION,
    AgentConfiguration,
    AgentConfigurationSchema,
)
from monkey_island.cc.repository import (
    IAgentConfigurationRepository,
    IFileRepository,
    RetrievalError,
)

AGENT_CONFIGURATION_FILE_NAME = "agent_configuration.json"


class FileAgentConfigurationRepository(IAgentConfigurationRepository):
    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository
        self._schema = AgentConfigurationSchema()

    def get_configuration(self) -> AgentConfiguration:
        try:
            with self._file_repository.open_file(AGENT_CONFIGURATION_FILE_NAME) as f:
                configuration_json = f.read().decode()

            return self._schema.loads(configuration_json)
        # TODO: Handle FileRetrievalError vs FileNotFoundError
        #       https://github.com/guardicore/monkey/blob/e8001d8cf76340e42bf17ff62523bd2d85fc4841/monkey/monkey_island/cc/repository/file_storage/local_storage_file_repository.py#L47-L50
        except RetrievalError:
            return self._schema.loads(DEFAULT_AGENT_CONFIGURATION)

    def store_configuration(self, agent_configuration: AgentConfiguration):
        configuration_json = self._schema.dumps(agent_configuration)

        self._file_repository.save_file(
            AGENT_CONFIGURATION_FILE_NAME, io.BytesIO(configuration_json.encode())
        )
