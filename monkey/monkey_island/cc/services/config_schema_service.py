from typing import Any, Dict

from common.agent_configuration import AgentConfiguration, PluginConfiguration
from common.agent_plugins import AgentPlugin, AgentPluginType
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

    def _create_plugin_schema(self, plugin: AgentPlugin) -> Dict[str, Any]:
        schema = PluginConfiguration.schema()
        schema["properties"]["name"]["enum"] = [plugin.plugin_manifest.name]
        schema["properties"]["options"]["properties"] = plugin.config_schema

        return schema

    def _add_plugins_to_schema(self, schema: Dict[str, Any]):
        # Note: Can throw RetrievalError, UnknownRecordError
        plugins = self._agent_plugin_repository.get_plugin_catalog()
        if plugins:
            schema["plugins"] = {}

        for (plugin_type, name) in plugins:
            plugin = self._agent_plugin_repository.get_plugin(plugin_type, name)
            plugin_schema = self._create_plugin_schema(plugin)

            plugin_type_name = str(plugin_type.name).lower()
            if plugin_type_name not in schema["plugins"]:
                schema["plugins"][plugin_type_name] = {"anyOf": []}
            schema["plugins"][plugin_type_name]["anyOf"].append(plugin_schema)

            # Add reference, based on type
            # TODO: It would actually probably be easier to forego the
            # reference and just add the schema here
            if plugin_type == AgentPluginType.EXPLOITER:
                exploitation = schema["definitions"]["ExploitationConfiguration"]
                brute_force = exploitation["properties"]["brute_force"]
                brute_force["items"] = {"$ref": "#/plugins/exploiter"}

    def get_schema(self) -> Dict[str, Any]:
        """
        Get the schema.

        :raises RuntimeError: If the schema could not be retrieved
        """
        try:
            agent_config_schema = AgentConfiguration.schema()

            self._add_plugins_to_schema(agent_config_schema)

            return agent_config_schema
        except Exception as err:
            raise RuntimeError(err)
