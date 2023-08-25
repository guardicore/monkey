import logging
from collections import defaultdict
from contextlib import suppress
from typing import Any, Dict, Optional

import gridfs
from bson.errors import BSONError
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType, PluginName
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
        self, host_operating_system: OperatingSystem, plugin_type: AgentPluginType, name: PluginName
    ) -> AgentPlugin:
        try:
            plugin_dict = self._get_agent_plugin(plugin_type, name)
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
        except UnknownRecordError:
            raise
        except Exception as err:
            raise RetrievalError(
                f"Error retrieving the agent plugin {name} of type {plugin_type} for operating "
                f"system {host_operating_system}: {err}"
            )

    def _get_agent_plugin(
        self, plugin_type: AgentPluginType, plugin_name: PluginName
    ) -> Dict[str, Any]:
        plugin_dict = self._agent_plugins_collection.find_one(
            {
                "plugin_manifest.name": plugin_name,
                "plugin_manifest.plugin_type": plugin_type.value,
            },
            {MONGO_OBJECT_ID_KEY: False},
        )

        if plugin_dict is None:
            raise UnknownRecordError(
                f"Error retrieving the agent plugin {plugin_name} of type {plugin_type}"
            )

        return plugin_dict

    def get_all_plugin_configuration_schemas(
        self,
    ) -> Dict[AgentPluginType, Dict[PluginName, Dict[str, Any]]]:
        try:
            configuration_schema_dicts = self._agent_plugins_collection.find(
                {},
                {"plugin_manifest.plugin_type": 1, "plugin_manifest.name": 1, "config_schema": 1},
            )
        except (PyMongoError, BSONError) as err:
            raise RetrievalError("Error retrieving the agent plugin configuration schemas") from err
        configuration_schemas: Dict[
            AgentPluginType, Dict[PluginName, Dict[str, Any]]
        ] = defaultdict(dict)

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

    def get_all_plugin_manifests(
        self,
    ) -> Dict[AgentPluginType, Dict[PluginName, AgentPluginManifest]]:
        try:
            manifest_dicts = self._agent_plugins_collection.find(projection=["plugin_manifest"])
        except (PyMongoError, BSONError) as err:
            raise RetrievalError("Error retrieving the agent plugin manifests") from err
        manifests: Dict[AgentPluginType, Dict[PluginName, AgentPluginManifest]] = defaultdict(dict)

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
        plugin_dict = agent_plugin.dict(simplify=True, exclude={"source_archive"})
        plugin_dict[BINARY_OS_MAPPING_KEY] = {}

        with suppress(UnknownRecordError):
            old_plugin = self._get_agent_plugin(plugin_type, plugin_name)
            try:
                self._remove_plugin_binary(old_plugin, operating_system)
            except Exception as err:
                raise StorageError(
                    f"Failed to remove old binary for plugin {plugin_name} of type {plugin_type} "
                    f"for operating system {operating_system}: {err}"
                )

        plugin_binary_ids = plugin_dict[BINARY_OS_MAPPING_KEY]
        try:
            _id = self._agent_plugins_binaries_collections[operating_system].put(
                agent_plugin.source_archive
            )
        except Exception as err:
            raise StorageError(
                f"Failed to store binary for plugin {plugin_name} of type {plugin_type} for "
                f"operating system {operating_system}"
            ) from err
        plugin_binary_ids[operating_system.value] = _id

        try:
            self._agent_plugins_collection.update_one(
                {
                    "plugin_manifest.name": plugin_name,
                    "plugin_manifest.plugin_type": plugin_type.value,
                },
                {"$set": plugin_dict},
                upsert=True,
            )
        except (PyMongoError, BSONError) as err:
            raise StorageError("Failed to store a plugin in the database") from err

    def remove_agent_plugin(
        self,
        agent_plugin_type: AgentPluginType,
        agent_plugin_name: PluginName,
        operating_system: Optional[OperatingSystem] = None,
    ):
        try:
            plugin_dict = self._get_agent_plugin(agent_plugin_type, agent_plugin_name)
            self._remove_agent_plugin(plugin_dict, operating_system)
        except UnknownRecordError:
            logger.debug(f"Plugin {agent_plugin_name} of type {agent_plugin_type} not found")
            return
        except Exception as err:
            raise RemovalError(
                f"Error removing the agent plugin {agent_plugin_name} of type {agent_plugin_type} "
                f"for operating system {operating_system}: {err}"
            )

    def _remove_agent_plugin(
        self, plugin_dict: Dict[str, Any], operating_system: Optional[OperatingSystem]
    ):
        self._remove_plugin_binary(plugin_dict, operating_system)
        # Update or delete the plugin record
        plugin_name = plugin_dict["plugin_manifest"]["name"]
        plugin_type = plugin_dict["plugin_manifest"]["plugin_type"]
        os_binaries = plugin_dict[BINARY_OS_MAPPING_KEY]
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

    def _remove_plugin_binary(
        self, plugin_dict: Dict[str, Any], operating_system: Optional[OperatingSystem]
    ):
        os_binaries = plugin_dict[BINARY_OS_MAPPING_KEY]

        if operating_system is None:
            os_binaries_to_remove = os_binaries.copy()
        elif operating_system.value not in os_binaries:
            return
        else:
            os_binaries_to_remove = {operating_system.value: os_binaries[operating_system.value]}

        for os, _id in os_binaries_to_remove.items():
            self._agent_plugins_binaries_collections[OperatingSystem(os)].delete(_id)
            os_binaries.pop(os)
