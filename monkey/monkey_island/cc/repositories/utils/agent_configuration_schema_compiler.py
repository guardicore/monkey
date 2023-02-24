from copy import deepcopy
from enum import Enum
from typing import Any, Dict, Type, cast

import dpath.util
import pydantic
from pydantic import BaseModel

from common import HARD_CODED_EXPLOITER_MANIFESTS
from common.agent_configuration import AgentConfiguration
from common.agent_plugins import AgentPluginManifest, AgentPluginType
from common.hard_coded_manifests.hard_coded_credential_collector_manifests import (
    HARD_CODED_CREDENTIAL_COLLECTOR_MANIFESTS,
)
from common.hard_coded_manifests.hard_coded_fingerprinter_manifests import (
    HARD_CODED_FINGERPRINTER_MANIFESTS,
)
from monkey_island.cc.repositories import IAgentPluginRepository
from monkey_island.cc.repositories.utils.hard_coded_credential_collector_schemas import (
    HARD_CODED_CREDENTIAL_COLLECTOR_SCHEMAS,
)
from monkey_island.cc.repositories.utils.hard_coded_exploiter_schemas import (
    HARD_CODED_EXPLOITER_SCHEMAS,
)
from monkey_island.cc.repositories.utils.hard_coded_fingerprinter_schemas import (
    HARD_CODED_FINGERPRINTER_SCHEMAS,
)

PLUGIN_PATH_IN_SCHEMA = {
    AgentPluginType.EXPLOITER: "definitions.ExploitationConfiguration.properties.exploiters",
    AgentPluginType.CREDENTIAL_COLLECTOR: "properties.credential_collectors",
    AgentPluginType.FINGERPRINTER: "definitions.NetworkScanConfiguration.properties.fingerprinters",
}


class AgentConfigurationSchemaCompiler:
    def __init__(self, agent_plugin_repository: IAgentPluginRepository):
        self._agent_plugin_repository = agent_plugin_repository

    def get_schema(self) -> Dict[str, Any]:
        try:
            AgentConfigurationSchemaCompiler._pydantic_schema_generation_override()
            agent_config_schema = AgentConfiguration.schema()
            agent_config_schema = self._add_plugins(agent_config_schema)

            return agent_config_schema
        except Exception as err:
            raise RuntimeError(err)

    @staticmethod
    def _pydantic_schema_generation_override():
        # See https://github.com/pydantic/pydantic/issues/5106
        from pydantic.schema import default_ref_template

        def model_process_schema_internal(
            model,
            *,
            by_alias: bool = True,
            generate_descriptions: bool = True,  # noqa: F841
            model_name_map,
            ref_prefix=None,
            ref_template: str = default_ref_template,  # type: ignore
            known_models=None,
            field=None,
        ):
            from inspect import signature

            known_models = known_models or set()
            from pydantic.utils import lenient_issubclass

            if lenient_issubclass(model, Enum):
                model = cast(Type[Enum], model)
                from pydantic.schema import enum_process_schema

                s = enum_process_schema(model, field=field)
                return s, {}, set()
            model = cast(Type["BaseModel"], model)
            s = {"title": model.__config__.title or model.__name__}
            known_models.add(model)
            from pydantic.schema import model_type_schema

            m_schema, m_definitions, nested_models = model_type_schema(
                model,
                by_alias=by_alias,
                model_name_map=model_name_map,
                ref_prefix=ref_prefix,
                ref_template=ref_template,
                known_models=known_models,
            )
            s.update(m_schema)
            schema_extra = model.__config__.schema_extra
            if callable(schema_extra):
                if len(signature(schema_extra).parameters) == 1:
                    schema_extra(s)
                else:
                    schema_extra(s, model)
            else:
                s.update(schema_extra)
            return s, m_definitions, nested_models

        pydantic.schema.model_process_schema = model_process_schema_internal

    def _add_plugins(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        schema = self._add_properties_field_to_plugin_types(schema)

        # Hard coded plugins need to be added manually. Remove all methods starting with
        # _add_non_plugin once they are turned into plugins
        schema = self._add_non_plugin_exploiters(schema)
        schema = self._add_non_plugin_fingerprinters(schema)
        schema = self._add_non_plugin_credential_collectors(schema)

        config_schemas = deepcopy(
            self._agent_plugin_repository.get_all_plugin_configuration_schemas()
        )

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

    def _add_manifests_to_plugins_schema(
        self, schema: Dict[str, Any], manifests: Dict[str, AgentPluginManifest]
    ) -> Dict[str, Any]:
        for plugin_name, manifest in manifests.items():
            schema[plugin_name].update(manifest.dict(simplify=True))
        return schema

    def _add_non_plugin_exploiters(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        properties = dpath.util.get(
            schema, PLUGIN_PATH_IN_SCHEMA[AgentPluginType.EXPLOITER] + ".properties", "."
        )
        exploiter_schemas = self._add_manifests_to_plugins_schema(
            HARD_CODED_EXPLOITER_SCHEMAS, HARD_CODED_EXPLOITER_MANIFESTS
        )
        properties.update(exploiter_schemas)
        return schema

    def _add_non_plugin_credential_collectors(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        properties = dpath.util.get(
            schema, PLUGIN_PATH_IN_SCHEMA[AgentPluginType.CREDENTIAL_COLLECTOR] + ".properties", "."
        )
        credential_collector_schemas = self._add_manifests_to_plugins_schema(
            HARD_CODED_CREDENTIAL_COLLECTOR_SCHEMAS, HARD_CODED_CREDENTIAL_COLLECTOR_MANIFESTS
        )
        properties.update(credential_collector_schemas)
        return schema

    def _add_non_plugin_fingerprinters(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        properties = dpath.util.get(
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
        properties = dpath.util.get(schema, PLUGIN_PATH_IN_SCHEMA[plugin_type] + ".properties", ".")
        properties.update({plugin_name: config_schema})
        return schema
