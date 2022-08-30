import io
import json

from common.agent_configuration import AgentConfiguration
from monkey_island.cc import repository
from monkey_island.cc.repository import (
    IAgentConfigurationRepository,
    IFileRepository,
    RetrievalError,
)

AGENT_CONFIGURATION_FILE_NAME = "agent_configuration.json"


class FileAgentConfigurationRepository(IAgentConfigurationRepository):
    def __init__(
        self, default_agent_configuration: AgentConfiguration, file_repository: IFileRepository
    ):
        self._default_agent_configuration = default_agent_configuration
        self._file_repository = file_repository

    def get_configuration(self) -> AgentConfiguration:
        try:
            with self._file_repository.open_file(AGENT_CONFIGURATION_FILE_NAME) as f:
                configuration_json = f.read().decode()

            return AgentConfiguration(**json.loads(configuration_json))
        except repository.FileNotFoundError:
            return self._default_agent_configuration
        except Exception as err:
            raise RetrievalError(f"Error retrieving the agent configuration: {err}")

    def store_configuration(self, agent_configuration: AgentConfiguration):
        configuration_json = agent_configuration.dict()

        self._file_repository.save_file(
            AGENT_CONFIGURATION_FILE_NAME, io.BytesIO(json.dumps(configuration_json).encode())
        )

    def reset_to_default(self):
        self.store_configuration(self._default_agent_configuration)
