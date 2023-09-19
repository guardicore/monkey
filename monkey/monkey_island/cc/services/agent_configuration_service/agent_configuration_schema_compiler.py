from copy import deepcopy
from typing import Any, Dict

import dpath

from common.agent_configuration import AgentConfiguration
from common.agent_plugins import AgentPluginManifest, AgentPluginType
from common.hard_coded_manifests.hard_coded_fingerprinter_manifests import (
    HARD_CODED_FINGERPRINTER_MANIFESTS,
)
from monkey_island.cc.services.agent_plugin_service import IAgentPluginService

from .hard_coded_schemas import HARD_CODED_FINGERPRINTER_SCHEMAS

PLUGIN_PATH_IN_SCHEMA = {
    AgentPluginType.EXPLOITER: "definitions.ExploitationConfiguration.properties.exploiters",
    AgentPluginType.CREDENTIALS_COLLECTOR: "properties.credentials_collectors",
    AgentPluginType.FINGERPRINTER: "definitions.NetworkScanConfiguration.properties.fingerprinters",
    AgentPluginType.PAYLOAD: "properties.payloads",
}


class AgentConfigurationSchemaCompiler:
    def __init__(self, agent_plugin_service: IAgentPluginService):
        self._agent_plugin_service = agent_plugin_service

    def get_schema(self) -> Dict[str, Any]:
        try:
            agent_config_schema = AgentConfiguration.schema()
            agent_config_schema = self._add_plugins(agent_config_schema)

            return agent_config_schema
        except Exception as err:
            raise RuntimeError(err)

    def _add_plugins(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        schema = self._add_properties_field_to_plugin_types(schema)

        # Hard coded plugins need to be added manually until they are refactored into
        # proper plugins
        schema = self._add_hard_coded_plugins(schema)

        config_schemas = deepcopy(self._agent_plugin_service.get_all_plugin_configuration_schemas())
        all_plugin_manifests = self._agent_plugin_service.get_all_plugin_manifests()

        for plugin_type in config_schemas.keys():
            for plugin_name in config_schemas[plugin_type].keys():
                config_schema = config_schemas[plugin_type][plugin_name]
                plugin_manifest = all_plugin_manifests[plugin_type][plugin_name]
                config_schema.update(plugin_manifest.dict(simplify=True))
                schema = self._add_plugin_to_schema(schema, plugin_type, plugin_name, config_schema)
        return schema

    def _add_hard_coded_plugins(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        schema = self._add_non_plugin_fingerprinters(schema)
        return schema

    def _add_properties_field_to_plugin_types(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        for plugin_path in PLUGIN_PATH_IN_SCHEMA.values():
            plugin_schema = dpath.get(schema, plugin_path, ".")
            plugin_schema["properties"] = {}
            plugin_schema["additionalProperties"] = False
        return schema

    def _add_manifests_to_plugins_schema(
        self, schema: Dict[str, Any], manifests: Dict[str, AgentPluginManifest]
    ) -> Dict[str, Any]:
        for plugin_name, manifest in manifests.items():
            schema[plugin_name].update(manifest.dict(simplify=True))
        return schema

    def _add_non_plugin_fingerprinters(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        properties = dpath.get(
            schema, PLUGIN_PATH_IN_SCHEMA[AgentPluginType.FINGERPRINTER] + ".properties", "."
        )
        fingerprinter_schemas = self._add_manifests_to_plugins_schema(
            HARD_CODED_FINGERPRINTER_SCHEMAS, HARD_CODED_FINGERPRINTER_MANIFESTS
        )
        properties.update(fingerprinter_schemas)
        return schema

    def _add_plugin_to_schema(
        self,
        schema: Dict[str, Any],
        plugin_type: AgentPluginType,
        plugin_name: str,
        config_schema: Dict[str, Any],
    ):
        properties = dpath.get(schema, PLUGIN_PATH_IN_SCHEMA[plugin_type] + ".properties", ".")
        properties.update({plugin_name: config_schema})
        return schema
