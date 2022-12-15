from typing import Any, Dict

from common.agent_configuration import AgentConfiguration
from monkey_island.cc.repositories import IAgentPluginRepository


class ConfigSchemaService:
    """
    A service for retrieving the agent configuration schema.
    """

    def __init__(
        self,
        agent_plugin_repository: IAgentPluginRepository,
    ):
        self._agent_plugin_repository = agent_plugin_repository

    def get_schema(self) -> Dict[str, Any]:
        """
        Get the schema.

        :raises RuntimeError: If the schema could not be retrieved
        """
        try:
            agent_config_schema = AgentConfiguration.schema()
            return agent_config_schema
        except Exception as err:
            raise RuntimeError(err)
