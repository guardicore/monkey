import logging
from enum import Enum
from typing import Any, Dict, Optional

import gridfs
from pymongo import MongoClient

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType
from monkey_island.cc.repositories import RetrievalError, StorageError, UnknownRecordError

from .i_agent_plugin_repository import IAgentPluginRepository

BINARY_OS_MAPPING_KEY = "binaries"

logger = logging.getLogger(__name__)


class MongoAgentPluginRepository(IAgentPluginRepository):
    def __init__(self, mongo_client: MongoClient) -> None:
        self._agent_plugins_collection = mongo_client.monkey_island.agent_plugins
        self._agent_plugins_binaries_collections = self._get_binary_collections(mongo_client)

    def _get_binary_collections(
        self, mongo_client: MongoClient
    ) -> Dict[OperatingSystem, gridfs.GridFS]:
        # Note: This expects the database to have a collection for each operating system
        agent_plugins_binaries_collections: Dict[OperatingSystem, gridfs.GridFS] = {}

        for os in OperatingSystem:
            agent_plugins_binaries_collections[os] = gridfs.GridFS(
                mongo_client.monkey_island, self._get_binary_collection_name(os)
            )

        return agent_plugins_binaries_collections

    def _get_binary_collection_name(self, operating_system: OperatingSystem) -> str:
        return f"agent_plugins_binaries_{operating_system.value}"

    def get_plugin(
        self, host_operating_system: OperatingSystem, plugin_type: AgentPluginType, name: str
    ) -> AgentPlugin:
        # TODO: Figure out how to store/load binaries for each operating system.
        #       - We can store a dict field with the ID of the binary for each operating system
        #       - We remove this field and add the
        # - Query the agent_plugins collection for the serialized plugin
        # - Get the binary ID for the given OS from the serialized plugin
        # - Query the agent_plugins_binaries collection for the binary
        # - Remove the binary mapping from the serialized plugin
        # - Add the binary to the serialized plugin
        # - Deserialize the plugin
        try:
            plugin_dict = self._get_agent_plugin(plugin_type, name)
        except Exception:
            raise UnknownRecordError(
                f"Error retrieving the agent plugin {name} of type {plugin_type}"
            )

        try:
            os_binaries = plugin_dict[BINARY_OS_MAPPING_KEY]
            id = os_binaries[host_operating_system.value]
            plugin_source_bytes = (
                self._agent_plugins_binaries_collections[host_operating_system].get(id).read()
            )

            plugin_dict.pop(BINARY_OS_MAPPING_KEY)
            plugin_dict.pop("_id")
            plugin_dict["source_archive"] = plugin_source_bytes
            return AgentPlugin(**plugin_dict)
        except Exception as err:
            raise RetrievalError(
                f"Error retrieving the agent plugin {name} of type {plugin_type} for operating "
                f"system {host_operating_system}: {err}"
            )

    def _get_agent_plugin(self, plugin_type: AgentPluginType, plugin_name: str) -> Dict[str, Any]:
        plugin_dict = self._agent_plugins_collection.find_one(
            {"plugin_manifest.name": plugin_name, "plugin_manifest.plugin_type": plugin_type.value}
        )
        if plugin_dict is None:
            raise RuntimeError("Not found")
        return plugin_dict

    def get_all_plugin_configuration_schemas(
        self,
    ) -> Dict[AgentPluginType, Dict[str, Dict[str, Any]]]:
        # TODO: Potentially use aggregation to get the config schemas
        configuration_schema_dicts = self._agent_plugins_collection.find(
            {}, {"plugin_manifest.type": 1, "plugin_manifest.name": 1, "config_schema": 1}
        )
        configuration_schemas: Dict[AgentPluginType, Dict[str, Dict[str, Any]]] = {}

        for item in configuration_schema_dicts:
            plugin_type = AgentPluginType(item["type"])
            plugin_name = item["name"]
            config_schema_dict = item["config_schema"]
            if plugin_type not in configuration_schemas:
                configuration_schemas[plugin_type] = {}
            configuration_schemas[plugin_type][plugin_name] = config_schema_dict

        return configuration_schemas

    def get_all_plugin_manifests(self) -> Dict[AgentPluginType, Dict[str, AgentPluginManifest]]:
        # TODO: Potentially use aggregation to get the manifests:
        # manifest_dicts = self._agent_plugins_collection.aggregate(
        #     [
        #         {
        #             "$group": {
        #                 "_id": "$plugin_manifest.plugin_type",
        #                 "items": {"$addToSet": "$plugin_manifest"},
        #             }
        #         }
        #     ]
        # )
        manifest_dicts = self._agent_plugins_collection.find({}, {"plugin_manifest": 1})
        manifests: Dict[AgentPluginType, Dict[str, AgentPluginManifest]] = {}

        for manifest_dict in manifest_dicts:
            manifest = AgentPluginManifest(**manifest_dict["plugin_manifest"])
            plugin_type = manifest.plugin_type
            plugin_name = manifest.name
            if plugin_type not in manifests:
                manifests[plugin_type] = {}
            manifests[plugin_type][plugin_name] = manifest

        return manifests

    def store_agent_plugin(self, operating_system: OperatingSystem, agent_plugin: AgentPlugin):
        # TODO:
        # - Query the agent_plugins collection for the serialized plugin
        # - ~Generate the binary for each supported OS~ This should already be done...
        # - Store the binary in the corresponding collection
        # - Construct a dict with the ID of the binary for each OS (or modify existing dict)
        # - Serialize the AgentPlugin to a dict (if not already in the collection)
        #   - Strip out the binary data
        #   - Add the binary dict to the serialized AgentPlugin
        # - Store the plugin in the agent_plugins collection (potentially updating existing record)
        plugin_name = agent_plugin.plugin_manifest.name
        plugin_type = agent_plugin.plugin_manifest.plugin_type
        try:
            plugin_dict = self._get_agent_plugin(plugin_type, plugin_name)
        except Exception:
            plugin_dict = self._encode_agent_plugin(agent_plugin)
            plugin_dict[BINARY_OS_MAPPING_KEY] = {}

        if operating_system.value in plugin_dict[BINARY_OS_MAPPING_KEY]:
            raise StorageError(
                f"Plugin {plugin_name} of type {plugin_type} already has a binary for "
                f"operating system {operating_system}"
            )

        try:
            id = self._agent_plugins_binaries_collections[operating_system].put(
                agent_plugin.source_archive
            )
            plugin_dict[BINARY_OS_MAPPING_KEY][operating_system.value] = id
        except Exception:
            raise StorageError(
                f"Failed to store binary for plugin {plugin_name} of type {plugin_type} for "
                f"operating system {operating_system}"
            )

        print(f"Writing plugin {plugin_dict}")
        self._agent_plugins_collection.update_one(
            {"plugin_manifest.name": plugin_name, "plugin_manifest.plugin_type": plugin_type.value},
            {"$set": plugin_dict},
            upsert=True,
        )

    def _encode_agent_plugin(self, agent_plugin: AgentPlugin) -> Dict[str, Any]:
        dict = agent_plugin.dict(simplify=True, exclude={"source_archive"})

        return self._encode_dict(dict)

    def _encode_dict(self, d: dict):
        new_dict = {}
        for k, v in d.items():
            if isinstance(k, Enum):
                k = k.value
            if isinstance(v, Enum):
                v = v.value
            if isinstance(v, dict):
                v = self._encode_dict(v)

            new_dict[k] = v

        return new_dict

    def remove_agent_plugin(
        self,
        agent_plugin_type: AgentPluginType,
        agent_plugin_name: str,
        operating_system: Optional[OperatingSystem] = None,
    ):
        raise NotImplementedError()
