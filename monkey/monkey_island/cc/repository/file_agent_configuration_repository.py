import io

from common.configuration import (
    DEFAULT_AGENT_CONFIGURATION,
    AgentConfiguration,
    AgentConfigurationSchema,
)
from monkey_island.cc import repository
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
        except repository.FileNotFoundError:
            return self._schema.loads(DEFAULT_AGENT_CONFIGURATION)
        except Exception as err:
            raise RetrievalError(f"Error retrieving the agent configuration: {err}")

    def store_configuration(self, agent_configuration: AgentConfiguration):
        configuration_json = self._schema.dumps(agent_configuration)

        self._file_repository.save_file(
            AGENT_CONFIGURATION_FILE_NAME, io.BytesIO(configuration_json.encode())
        )
