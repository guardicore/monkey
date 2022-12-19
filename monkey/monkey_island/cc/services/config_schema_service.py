from copy import deepcopy
from typing import Any, Dict, Sequence, Tuple

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

    def get_schema(self) -> Dict[str, Any]:
        """
        Get the schema.

        :raises RuntimeError: If the schema could not be retrieved
        """
        try:
            agent_config_schema = deepcopy(AgentConfiguration.schema())

            self._add_plugins_to_schema(agent_config_schema)

            return agent_config_schema
        except Exception as err:
            raise RuntimeError(err)

    def _add_plugins_to_schema(self, schema: Dict[str, Any]):
        plugin_catalog = self._agent_plugin_repository.get_plugin_catalog()
        if plugin_catalog:
            schema["definitions"].setdefault("AgentPluginsConfiguration", {})
            schema["definitions"]["AgentPluginsConfiguration"][
                "title"
            ] = "AgentPluginsConfiguration"
            schema["definitions"]["AgentPluginsConfiguration"]["type"] = "object"
            schema["definitions"]["AgentPluginsConfiguration"]["description"] = (
                "A configuration for agent plugins.\n It provides a full"
                " set of available plugins that can be used by the agent.\n"
            )

        self._set_exploiters_reference(schema, plugin_catalog)

        for (plugin_type, name) in plugin_catalog:
            plugin = self._agent_plugin_repository.get_plugin(plugin_type, name)
            plugin_schema = self._create_plugin_schema(plugin)

            plugin_type_name = plugin_type.name.lower()
            plugin_type_schema = schema["definitions"]["AgentPluginsConfiguration"].setdefault(
                plugin_type_name, {}
            )
            plugin_type_schema.setdefault("anyOf", []).append(plugin_schema)

    def _set_exploiters_reference(
        self, schema: Dict[str, Any], plugin_catalog: Sequence[Tuple[AgentPluginType, str]]
    ):
        plugin_types = set([plugin_type for (plugin_type, _) in plugin_catalog])

        for plugin_type in plugin_types:
            # Add reference, based on type
            if plugin_type == AgentPluginType.EXPLOITER:
                exploitation = schema["definitions"]["ExploitationConfiguration"]
                brute_force = exploitation["properties"]["brute_force"]
                brute_force["items"] = {"$ref": "#/definitions/AgentPluginsConfiguration/exploiter"}
            else:
                raise Exception("Error occurred while getting configuration schema")

    def _create_plugin_schema(self, plugin: AgentPlugin) -> Dict[str, Any]:
        schema = deepcopy(PluginConfiguration.schema())
        schema["properties"]["name"]["enum"] = [plugin.plugin_manifest.name]
        schema["properties"]["options"]["properties"] = plugin.config_schema

        return schema
