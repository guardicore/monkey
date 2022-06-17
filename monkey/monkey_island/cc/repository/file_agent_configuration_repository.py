import io

from common.configuration import AgentConfiguration, AgentConfigurationSchema
from monkey_island.cc.repository import IAgentConfigurationRepository, IFileRepository

AGENT_CONFIGURATION_FILE_NAME = "agent_configuration.json"


class FileAgentConfigurationRepository(IAgentConfigurationRepository):
    def __init__(self, file_repository: IFileRepository):
        self._file_repository = file_repository
        self._schema = AgentConfigurationSchema()

    def get_configuration(self) -> AgentConfiguration:
        with self._file_repository.open_file(AGENT_CONFIGURATION_FILE_NAME) as f:
            configuration_json = f.read().decode()

        return self._schema.loads(configuration_json)

    def set_configuration(self, agent_configuration: AgentConfiguration):
        configuration_json = self._schema.dumps(agent_configuration)

        self._file_repository.save_file(
            AGENT_CONFIGURATION_FILE_NAME, io.BytesIO(configuration_json.encode())
        )
