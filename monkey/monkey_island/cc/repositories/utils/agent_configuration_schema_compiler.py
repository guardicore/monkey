from typing import Any, Dict

import dpath.util

from common.agent_configuration import AgentConfiguration
from common.agent_plugins import AgentPluginType
from monkey_island.cc.repositories import IAgentPluginRepository
from monkey_island.cc.repositories.utils.hard_coded_exploiters import HARD_CODED_EXPLOITER_PLUGINS

PLUGIN_PATH_IN_SCHEMA = {
    AgentPluginType.EXPLOITER: "definitions.ExploitationConfiguration.properties.exploiters"
}


class AgentConfigurationSchemaCompiler:
    def __init__(
        self,
        agent_plugin_repository: IAgentPluginRepository,
    ):
        self._agent_plugin_repository = agent_plugin_repository

    def get_schema(self) -> Dict[str, Any]:
        try:
            agent_config_schema = AgentConfiguration.schema()
            agent_config_schema = self._add_plugins(agent_config_schema)

            return agent_config_schema
        except Exception as err:
            raise RuntimeError(err)

    def _add_plugins(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        schema = self._add_properties_field_to_plugin_types(schema)
        schema = self._add_non_plugin_exploiters(schema)
        config_schemas = self._agent_plugin_repository.get_all_plugin_configuration_schemas()

        for plugin_type in config_schemas.keys():
            for plugin_name in config_schemas[plugin_type].keys():
                config_schema = config_schemas[plugin_type][plugin_name]
                schema = self._add_plugin_to_schema(schema, plugin_type, plugin_name, config_schema)

        return schema

    def _add_properties_field_to_plugin_types(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        for plugin_path in PLUGIN_PATH_IN_SCHEMA.values():
            plugin_schema = dpath.util.get(schema, plugin_path, ".")
            plugin_schema["properties"] = {}
            plugin_schema["additionalProperties"] = False
        return schema

    # Exploiters that are not plugins need to be added manually. This should be removed
    # once all exploiters are turned into plugins
    def _add_non_plugin_exploiters(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        properties = dpath.util.get(
            schema, PLUGIN_PATH_IN_SCHEMA[AgentPluginType.EXPLOITER] + ".properties", "."
        )
        properties.update(HARD_CODED_EXPLOITER_PLUGINS)
        return schema

    def _add_plugin_to_schema(
        self,
        schema: Dict[str, Any],
        plugin_type: AgentPluginType,
        plugin_name: str,
        config_schema: Dict[str, Any],
    ):
        properties = dpath.util.get(schema, PLUGIN_PATH_IN_SCHEMA[plugin_type] + ".properties", ".")
        properties.update({plugin_name: config_schema})
        return schema
