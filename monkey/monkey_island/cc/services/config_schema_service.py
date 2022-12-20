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
        """
        Add all plugins to the schema provided,

        :param schema: The schema which will be modified
        """
        plugin_catalog = self._agent_plugin_repository.get_plugin_catalog()

        self._set_plugin_type_schema(schema, plugin_catalog)

        for (plugin_type, name) in plugin_catalog:
            plugin = self._agent_plugin_repository.get_plugin(plugin_type, name)

            plugin_type_name = plugin_type.name.lower()
            schema["definitions"][plugin_type_name]["properties"].setdefault(
                name, self._create_plugin_schema(plugin)
            )

    def _set_plugin_type_schema(
        self, schema: Dict[str, Any], plugin_catalog: Sequence[Tuple[AgentPluginType, str]]
    ):
        """
        Modifies main schema with plugin schema and reference based on plugin type.

        :param schema: The schema which will be modified
        :param plugin_catalog: The catalog with all available plugin types and name
        :raises Exception: When unsupported plugin type is provided
        """
        plugin_types = set([plugin_type for (plugin_type, _) in plugin_catalog])

        for plugin_type in plugin_types:
            if plugin_type == AgentPluginType.EXPLOITER:
                plugin_type_name = plugin_type.name.lower()
                # Add exploiter definition
                self._set_exploiter_definition(schema, plugin_type_name)

                # Add exploiter reference to brute_force
                # TODO: Remove distinction in exploiter and change the reference
                exploitation = schema["definitions"]["ExploitationConfiguration"]
                exploitation["properties"]["brute_force"] = {
                    "$ref": f"#/definitions/{plugin_type_name}"
                }
            else:
                raise Exception(
                    "Error occurred while setting schema for {plugin_type} plugin type."
                )

    def _set_exploiter_definition(self, schema: Dict[str, Any], plugin_type_name: str):
        """
        Construct exploiter plugins schema.

        :param schema: The schema which will be modified
        :param plugin_type_name: The plugin type name used in the schema
        """
        plugin_type_schema = schema["definitions"].setdefault(plugin_type_name, {})
        plugin_type_schema["title"] = "Exploiter Plugins"
        plugin_type_schema["type"] = "object"
        plugin_type_schema["description"] = (
            "A configuration for agent exploiter plugins.\n It provides a full"
            " set of available exploiter plugins that can be used by the agent.\n"
        )
        plugin_type_schema.setdefault("properties", {})

    def _create_plugin_schema(self, plugin: AgentPlugin) -> Dict[str, Any]:
        """
        Generate plugin configuration schema.

        :param plugin: The AgentPlugin for which we generate the schema
        """
        schema = deepcopy(PluginConfiguration.schema())
        schema["properties"]["name"]["title"] = plugin.plugin_manifest.title
        schema["properties"]["options"]["properties"] = plugin.config_schema
        return schema
