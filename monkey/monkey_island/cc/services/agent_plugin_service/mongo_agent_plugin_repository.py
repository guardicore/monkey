import logging
from collections import defaultdict
from typing import Any, Dict, Optional

import gridfs
from pymongo import MongoClient

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType
from monkey_island.cc.repositories import (
    RemovalError,
    RetrievalError,
    StorageError,
    UnknownRecordError,
)
from monkey_island.cc.repositories.consts import MONGO_OBJECT_ID_KEY

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
        try:
            plugin_dict = self._get_agent_plugin(plugin_type, name)
        except Exception:
            raise UnknownRecordError(
                f"Error retrieving the agent plugin {name} of type {plugin_type}"
            )

        try:
            os_binaries = plugin_dict[BINARY_OS_MAPPING_KEY]
            gridfs_file_id = os_binaries[host_operating_system.value]
            plugin_source_bytes = (
                self._agent_plugins_binaries_collections[host_operating_system]
                .get(gridfs_file_id)
                .read()
            )

            plugin_dict.pop(BINARY_OS_MAPPING_KEY)
            plugin_dict["source_archive"] = plugin_source_bytes
            return AgentPlugin(**plugin_dict)
        except Exception as err:
            raise RetrievalError(
                f"Error retrieving the agent plugin {name} of type {plugin_type} for operating "
                f"system {host_operating_system}: {err}"
            )

    def _get_agent_plugin(self, plugin_type: AgentPluginType, plugin_name: str) -> Dict[str, Any]:
        plugin_dict = self._agent_plugins_collection.find_one(
            {"plugin_manifest.name": plugin_name, "plugin_manifest.plugin_type": plugin_type.value},
            {MONGO_OBJECT_ID_KEY: False},
        )
        if plugin_dict is None:
            raise RuntimeError("Not found")
        return plugin_dict

    def get_all_plugin_configuration_schemas(
        self,
    ) -> Dict[AgentPluginType, Dict[str, Dict[str, Any]]]:
        configuration_schema_dicts = self._agent_plugins_collection.find(
            {}, {"plugin_manifest.plugin_type": 1, "plugin_manifest.name": 1, "config_schema": 1}
        )
        configuration_schemas: Dict[AgentPluginType, Dict[str, Dict[str, Any]]] = defaultdict(dict)

        for item in configuration_schema_dicts:
            try:
                plugin_type = AgentPluginType(item["plugin_manifest"]["plugin_type"])
            except ValueError:
                raise RetrievalError(
                    f"Invalid plugin type stored in the database:"
                    f" {item['plugin_manifest']['plugin_type']}"
                )
            plugin_name = item["plugin_manifest"]["name"]
            config_schema_dict = item["config_schema"]
            configuration_schemas[plugin_type][plugin_name] = config_schema_dict

        return configuration_schemas

    def get_all_plugin_manifests(self) -> Dict[AgentPluginType, Dict[str, AgentPluginManifest]]:
        manifest_dicts = self._agent_plugins_collection.find(projection=["plugin_manifest"])
        manifests: Dict[AgentPluginType, Dict[str, AgentPluginManifest]] = defaultdict(dict)

        for manifest_dict in manifest_dicts:
            try:
                manifest = AgentPluginManifest(**manifest_dict["plugin_manifest"])
            except Exception as err:
                raise RetrievalError(
                    f"Can't create plugin manifest from the data in the database: {err}"
                )
            plugin_type = manifest.plugin_type
            plugin_name = manifest.name
            manifests[plugin_type][plugin_name] = manifest

        return manifests

    def store_agent_plugin(self, operating_system: OperatingSystem, agent_plugin: AgentPlugin):
        plugin_name = agent_plugin.plugin_manifest.name
        plugin_type = agent_plugin.plugin_manifest.plugin_type
        try:
            plugin_dict = self._get_agent_plugin(plugin_type, plugin_name)
        except Exception:
            plugin_dict = agent_plugin.dict(simplify=True, exclude={"source_archive"})
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

        self._agent_plugins_collection.update_one(
            {"plugin_manifest.name": plugin_name, "plugin_manifest.plugin_type": plugin_type.value},
            {"$set": plugin_dict},
            upsert=True,
        )

    def remove_agent_plugin(
        self,
        agent_plugin_type: AgentPluginType,
        agent_plugin_name: str,
        operating_system: Optional[OperatingSystem] = None,
    ):
        try:
            plugin_dict = self._get_agent_plugin(agent_plugin_type, agent_plugin_name)
        except Exception:
            logger.debug(f"Plugin {agent_plugin_name} of type {agent_plugin_type} not found")
            return

        try:
            self._remove_agent_plugin(plugin_dict, operating_system)
        except Exception as err:
            raise RemovalError(
                f"Error removing the agent plugin {agent_plugin_name} of type {agent_plugin_type} "
                f"for operating system {operating_system}: {err}"
            )

    def _remove_agent_plugin(
        self, plugin_dict: Dict[str, Any], operating_system: Optional[OperatingSystem]
    ):
        os_binaries = plugin_dict[BINARY_OS_MAPPING_KEY]

        if operating_system is None:
            os_binaries_to_remove = os_binaries.copy()
        else:
            os_binaries_to_remove = {operating_system.value: os_binaries[operating_system.value]}

        for os, id in os_binaries_to_remove.items():
            self._agent_plugins_binaries_collections[OperatingSystem(os)].delete(id)
            os_binaries.pop(os)

        # Update or delete the plugin record
        plugin_name = plugin_dict["plugin_manifest"]["name"]
        plugin_type = plugin_dict["plugin_manifest"]["plugin_type"]
        if len(os_binaries) == 0:
            self._agent_plugins_collection.delete_one(
                {
                    "plugin_manifest.name": plugin_name,
                    "plugin_manifest.plugin_type": plugin_type,
                }
            )
        else:
            self._agent_plugins_collection.update_one(
                {
                    "plugin_manifest.name": plugin_name,
                    "plugin_manifest.plugin_type": plugin_type,
                },
                {"$set": plugin_dict},
            )
