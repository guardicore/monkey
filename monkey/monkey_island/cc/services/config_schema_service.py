from copy import deepcopy
from typing import Any, Dict

from common.agent_configuration import AgentConfiguration
from common.agent_plugins import AgentPlugin, AgentPluginType
from monkey_island.cc.repositories import IAgentPluginRepository

PLUGIN_SCHEMAS = {
    AgentPluginType.EXPLOITER: {
        "title": "Exploiter Plugins",
        "type": "object",
        "description": "A configuration for agent exploiter plugins.\n It provides a full"
        " set of available exploiter plugins"
        " that can be used by the agent.\n",
        "properties": {},
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
            agent_config_schema = deepcopy(AgentConfiguration.schema())

            self._add_plugins_to_schema(agent_config_schema)

            return agent_config_schema
        except Exception as err:
            raise RuntimeError(err)

    def _add_plugins_to_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        plugin_catalog = self._agent_plugin_repository.get_plugin_catalog()

        for (plugin_type, name) in plugin_catalog:
            schema = self._inject_plugin_references_to_schema(plugin_type, schema)
            plugin = self._agent_plugin_repository.get_plugin(plugin_type, name)
            schema = self._add_plugin_to_schema(schema, plugin_type, plugin)

        return schema

    def _inject_plugin_references_to_schema(
        self, plugin_type: AgentPluginType, schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        if plugin_type == AgentPluginType.EXPLOITER:
            schema = self._set_exploiter_definition(schema, plugin_type)

            exploitation = schema["definitions"]["ExploitationConfiguration"]
            exploitation["properties"]["brute_force"] = {
                "$ref": f"#/definitions/{self._get_plugin_type_string(plugin_type)}"
            }
        else:
            raise NotImplementedError(
                f"Only plugins of type {AgentPluginType.EXPLOITER} are "
                f"supported. Type provided {plugin_type}"
            )

        return schema

    def _set_exploiter_definition(
        self, schema: Dict[str, Any], plugin_type: AgentPluginType
    ) -> Dict[str, Any]:
        plugin_type_string = self._get_plugin_type_string(plugin_type)
        if plugin_type_string not in schema["definitions"]:
            try:
                schema["definitions"][plugin_type_string] = PLUGIN_SCHEMAS[plugin_type]
            except KeyError:
                raise NotImplementedError(
                    f"Only plugins of type {AgentPluginType.EXPLOITER} are "
                    f"supported. Type provided {plugin_type}"
                )
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
