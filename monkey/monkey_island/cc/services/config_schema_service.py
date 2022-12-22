from typing import Any, Dict

import dpath.util

from common.agent_configuration import AgentConfiguration
from common.agent_plugins import AgentPlugin, AgentPluginType
from monkey_island.cc.repositories import IAgentPluginRepository

SUPPORTED_PLUGINS = {
    AgentPluginType.EXPLOITER: {
        "subschema": {
            "title": "Exploiter Plugins",
            "type": "object",
            "description": "A configuration for agent exploiter plugins.\n It provides a full"
            " set of available exploiter plugins"
            " that can be used by the agent.\n",
            "properties": {},
        },
        "path_in_schema": "definitions.ExploitationConfiguration.properties.brute_force",
    }
}


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
        Get the Agent configuration schema.

        :raises RuntimeError: If the schema could not be retrieved
        """
        try:
            agent_config_schema = AgentConfiguration.schema()
            agent_config_schema = self._add_plugin_defs(agent_config_schema)
            agent_config_schema = self._add_references_to_plugin_defs(agent_config_schema)
            agent_config_schema = self._add_plugins(agent_config_schema)

            return agent_config_schema
        except Exception as err:
            raise RuntimeError(err)

    def _add_plugin_defs(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        for plugin_type, subschema_info in SUPPORTED_PLUGINS.items():
            plugin_type_string = self._get_plugin_type_string(plugin_type)
            schema["definitions"][plugin_type_string] = SUPPORTED_PLUGINS[plugin_type]["subschema"]
        return schema

    def _add_references_to_plugin_defs(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        for plugin_type, subschema_info in SUPPORTED_PLUGINS.items():
            reference = {"$ref": f"#/definitions/{self._get_plugin_type_string(plugin_type)}"}
            dpath.util.set(schema, subschema_info["path_in_schema"], reference)

        return schema

    def _add_plugins(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        plugin_catalog = self._agent_plugin_repository.get_plugin_catalog()

        for (plugin_type, name) in plugin_catalog:
            plugin = self._agent_plugin_repository.get_plugin(plugin_type, name)
            schema = self._add_plugin_to_schema(schema, plugin_type, plugin)

        return schema

    @staticmethod
    def _get_plugin_type_string(plugin_type: AgentPluginType):
        return plugin_type.name.lower()

    def _add_plugin_to_schema(
        self, schema: Dict[str, Any], plugin_type: AgentPluginType, plugin: AgentPlugin
    ):
        plugin_type_string = self._get_plugin_type_string(plugin_type)
        schema["definitions"][plugin_type_string]["properties"][
            plugin.plugin_manifest.name
        ] = plugin.config_schema
        return schema
