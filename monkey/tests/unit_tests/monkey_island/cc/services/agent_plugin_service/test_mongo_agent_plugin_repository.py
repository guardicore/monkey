import copy
from typing import Dict
from unittest.mock import MagicMock

import gridfs
import mongomock
import pytest
from mongomock.gridfs import enable_gridfs_integration
from tests.data_for_tests.agent_plugin.manifests import (
    CREDENTIALS_COLLECTOR_MANIFEST_1,
    CREDENTIALS_COLLECTOR_NAME_1,
    EXPLOITER_MANIFEST_1,
    EXPLOITER_MANIFEST_2,
    EXPLOITER_NAME_1,
    EXPLOITER_NAME_2,
)
from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import FAKE_NAME
from tests.unit_tests.monkey_island.cc.fake_agent_plugin_data import (
    FAKE_AGENT_PLUGIN_1,
    FAKE_PLUGIN_CONFIG_SCHEMA_1,
)

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginType
from monkey_island.cc.repositories import (
    RemovalError,
    RetrievalError,
    StorageError,
    UnknownRecordError,
)
from monkey_island.cc.services.agent_plugin_service.mongo_agent_plugin_repository import (
    MongoAgentPluginRepository,
)

enable_gridfs_integration()

EXPECTED_MANIFEST = EXPLOITER_MANIFEST_1


@pytest.fixture
def mongo_client():
    client = mongomock.MongoClient()

    return client


@pytest.fixture
def binary_collections(mongo_client) -> Dict[OperatingSystem, gridfs.GridFS]:
    collections = {}
    for os in OperatingSystem:
        collections[os] = gridfs.GridFS(
            mongo_client.monkey_island, f"agent_plugins_binaries_{os.value}"
        )
    return collections


plugin_manifest_dict = EXPLOITER_MANIFEST_1.dict(simplify=True)
plugin_schema_dict = FAKE_PLUGIN_CONFIG_SCHEMA_1

basic_plugin_dict = {
    "plugin_manifest": plugin_manifest_dict,
    "config_schema": plugin_schema_dict,
    "supported_operating_systems": ("windows",),
}

malformed_plugin_dict = copy.deepcopy(basic_plugin_dict)
del malformed_plugin_dict["plugin_manifest"]["title"]
malformed_plugin_dict["plugin_manifest"]["tile"] = "dummy-exploiter"

typo_in_type_plugin_dict = copy.deepcopy(basic_plugin_dict)
del typo_in_type_plugin_dict["plugin_manifest"]["plugin_type"]
typo_in_type_plugin_dict["plugin_manifest"]["plugin_type"] = "credential_collector"


@pytest.fixture
def insert_plugin(mongo_client):
    def impl(file, operating_system: OperatingSystem, plugin_dict=None):
        if plugin_dict is None:
            plugin_dict = copy.deepcopy(basic_plugin_dict)
        binaries_collection = gridfs.GridFS(
            mongo_client.monkey_island, f"agent_plugins_binaries_{operating_system.value}"
        )
        id = binaries_collection.put(file)
        if "binaries" not in plugin_dict:
            plugin_dict["binaries"] = {}
        plugin_dict["binaries"][f"{operating_system.value}"] = id
        plugin_manifest_dict = plugin_dict["plugin_manifest"]
        mongo_client.monkey_island.agent_plugins.update_one(
            {
                "plugin_manifest.plugin_type": plugin_manifest_dict["plugin_type"],
                "plugin_manifest.name": plugin_manifest_dict["name"],
            },
            update={"$set": plugin_dict},
            upsert=True,
        )

        return plugin_dict

    return impl


@pytest.fixture
def agent_plugin_repository(mongo_client) -> MongoAgentPluginRepository:
    return MongoAgentPluginRepository(mongo_client)


@pytest.mark.slow
def test_get_plugin(
    plugin_file, insert_plugin, agent_plugin_repository: MongoAgentPluginRepository
):
    with open(plugin_file, "rb") as file:
        insert_plugin(file, OperatingSystem.WINDOWS)
    plugin = agent_plugin_repository.get_plugin(
        OperatingSystem.WINDOWS, AgentPluginType.EXPLOITER, EXPLOITER_NAME_1
    )

    assert plugin.plugin_manifest == EXPECTED_MANIFEST
    assert isinstance(plugin.config_schema, dict)
    assert len(plugin.source_archive) == 10240


def test_get_plugin__UnknownRecordError_if_not_exist(agent_plugin_repository):
    with pytest.raises(UnknownRecordError):
        agent_plugin_repository.get_plugin(
            OperatingSystem.WINDOWS, AgentPluginType.EXPLOITER, "does_not_exist"
        )


def test_get_plugin__RetrievalError_if_bad_plugin(
    plugin_file, insert_plugin, agent_plugin_repository: MongoAgentPluginRepository
):
    with open(plugin_file, "rb") as file:
        insert_plugin(file, OperatingSystem.WINDOWS, malformed_plugin_dict)

    with pytest.raises(RetrievalError):
        agent_plugin_repository.get_plugin(
            OperatingSystem.WINDOWS, AgentPluginType.EXPLOITER, EXPLOITER_NAME_1
        )


def test_get_plugin__RetrievalError_if_unsupported_os(
    plugin_file, insert_plugin, mongo_client, agent_plugin_repository: MongoAgentPluginRepository
):
    with open(plugin_file, "rb") as file:
        insert_plugin(file, OperatingSystem.WINDOWS)
    with pytest.raises(RetrievalError):
        agent_plugin_repository.get_plugin(
            OperatingSystem.LINUX, AgentPluginType.EXPLOITER, EXPLOITER_NAME_1
        )


def test_get_all_plugin_manifests(plugin_file, insert_plugin, agent_plugin_repository):
    dict1 = copy.deepcopy(basic_plugin_dict)
    dict2 = copy.deepcopy(basic_plugin_dict)
    dict2["plugin_manifest"] = EXPLOITER_MANIFEST_2.dict(simplify=True)
    dict3 = copy.deepcopy(basic_plugin_dict)
    dict3["plugin_manifest"] = CREDENTIALS_COLLECTOR_MANIFEST_1.dict(simplify=True)

    with open(plugin_file, "rb") as file:
        insert_plugin(file, OperatingSystem.WINDOWS, dict1)
        insert_plugin(file, OperatingSystem.WINDOWS, dict2)
        insert_plugin(file, OperatingSystem.WINDOWS, dict3)
        insert_plugin(file, OperatingSystem.LINUX, dict3)

    retrieved_plugin_manifests = agent_plugin_repository.get_all_plugin_manifests()

    assert (
        retrieved_plugin_manifests[AgentPluginType.EXPLOITER][EXPLOITER_NAME_1] == EXPECTED_MANIFEST
    )
    assert retrieved_plugin_manifests[AgentPluginType.CREDENTIALS_COLLECTOR] == {
        CREDENTIALS_COLLECTOR_NAME_1: CREDENTIALS_COLLECTOR_MANIFEST_1
    }


def test_get_all_plugin_manifests__RetrievalError_if_bad_plugin_type(
    plugin_file, insert_plugin, agent_plugin_repository
):
    dict1 = copy.deepcopy(typo_in_type_plugin_dict)

    with open(plugin_file, "rb") as file:
        insert_plugin(file, OperatingSystem.WINDOWS, dict1)

    with pytest.raises(RetrievalError):
        agent_plugin_repository.get_all_plugin_manifests()


def test_get_all_plugin_configuration_schemas(plugin_file, insert_plugin, agent_plugin_repository):
    dict1 = copy.deepcopy(basic_plugin_dict)
    dict2 = copy.deepcopy(basic_plugin_dict)
    dict2["plugin_manifest"] = EXPLOITER_MANIFEST_2.dict(simplify=True)

    with open(plugin_file, "rb") as file:
        insert_plugin(file, OperatingSystem.WINDOWS, dict1)
        insert_plugin(file, OperatingSystem.WINDOWS, dict2)

    retrieved_plugin_configuration_schemas = (
        agent_plugin_repository.get_all_plugin_configuration_schemas()
    )

    assert (
        retrieved_plugin_configuration_schemas[AgentPluginType.EXPLOITER][EXPLOITER_NAME_1]
        == FAKE_PLUGIN_CONFIG_SCHEMA_1
    )

    assert (
        retrieved_plugin_configuration_schemas[AgentPluginType.EXPLOITER][EXPLOITER_NAME_2]
        == FAKE_PLUGIN_CONFIG_SCHEMA_1
    )


def test_get_all_plugin_configuration_schemas__RetrievalError_if_bad_plugin_type(
    plugin_file, insert_plugin, agent_plugin_repository
):
    dict1 = copy.deepcopy(typo_in_type_plugin_dict)

    with open(plugin_file, "rb") as file:
        insert_plugin(file, OperatingSystem.WINDOWS, dict1)

    with pytest.raises(RetrievalError):
        agent_plugin_repository.get_all_plugin_configuration_schemas()


def test_store_agent_plugin(agent_plugin_repository: MongoAgentPluginRepository):
    agent_plugin_repository.store_agent_plugin(OperatingSystem.LINUX, FAKE_AGENT_PLUGIN_1)

    plugin = agent_plugin_repository.get_plugin(
        OperatingSystem.LINUX, AgentPluginType.EXPLOITER, FAKE_NAME
    )
    assert plugin == FAKE_AGENT_PLUGIN_1


def test_store_agent_plugin__storeageerror_if_binary_already_exists(
    plugin_file, insert_plugin, agent_plugin_repository: MongoAgentPluginRepository
):
    with open(plugin_file, "rb") as file:
        insert_plugin(file, OperatingSystem.WINDOWS)

    plugin_dict = copy.deepcopy(basic_plugin_dict)
    plugin_dict["source_archive"] = b"dummy"
    with pytest.raises(StorageError):
        agent_plugin_repository.store_agent_plugin(
            OperatingSystem.WINDOWS, AgentPlugin(**plugin_dict)
        )


def test_store_agent_plugin__storeageerror_if_binary_cannot_be_stored(
    mongo_client, agent_plugin_repository
):
    mongo_client.monkey_island.agent_plugins_binaries_linux.files.insert_one = MagicMock(
        side_effect=Exception("foo")
    )
    with pytest.raises(StorageError):
        agent_plugin_repository.store_agent_plugin(OperatingSystem.LINUX, FAKE_AGENT_PLUGIN_1)


def test_remove_agent_plugin(
    plugin_file,
    insert_plugin,
    mongo_client,
    agent_plugin_repository: MongoAgentPluginRepository,
):
    with open(plugin_file, "rb") as file:
        insert_plugin(file, OperatingSystem.WINDOWS)

    agent_plugin_repository.remove_agent_plugin(
        AgentPluginType.EXPLOITER, EXPLOITER_NAME_1, OperatingSystem.WINDOWS
    )

    # Assert
    agent_plugin = mongo_client.monkey_island.agent_plugins.find_one(
        {"plugin_manifest.name": EXPLOITER_NAME_1, "plugin_manifest.plugin_type": "Exploiter"}
    )
    assert agent_plugin is None
    assert mongo_client.monkey_island.agent_plugins_binaries_windows.files.count_documents({}) == 0


def test_remove_agent_plugin__removes_all_if_no_os_specified(
    plugin_file,
    insert_plugin,
    mongo_client,
    agent_plugin_repository: MongoAgentPluginRepository,
):
    with open(plugin_file, "rb") as file:
        plugin_dict = insert_plugin(file, OperatingSystem.WINDOWS)
        plugin_dict = insert_plugin(file, OperatingSystem.LINUX, plugin_dict)

    agent_plugin_repository.remove_agent_plugin(AgentPluginType.EXPLOITER, EXPLOITER_NAME_1)

    # Assert
    agent_plugin = mongo_client.monkey_island.agent_plugins.find_one(
        {"plugin_manifest.name": EXPLOITER_NAME_1, "plugin_manifest.plugin_type": "Exploiter"}
    )
    assert agent_plugin is None
    assert mongo_client.monkey_island.agent_plugins_binaries_linux.files.count_documents({}) == 0
    assert mongo_client.monkey_island.agent_plugins_binaries_windows.files.count_documents({}) == 0


def test_remove_agent_plugin__removes_one_if_os_specified(
    plugin_file, insert_plugin, mongo_client, agent_plugin_repository
):
    with open(plugin_file, "rb") as file:
        plugin_dict = insert_plugin(file, OperatingSystem.WINDOWS)
        plugin_dict = insert_plugin(file, OperatingSystem.LINUX, plugin_dict)

    agent_plugin_repository.remove_agent_plugin(
        AgentPluginType.EXPLOITER, EXPLOITER_NAME_1, OperatingSystem.WINDOWS
    )

    # Assert
    agent_plugin = mongo_client.monkey_island.agent_plugins.find_one(
        {"plugin_manifest.name": EXPLOITER_NAME_1, "plugin_manifest.plugin_type": "Exploiter"}
    )
    assert agent_plugin is not None
    assert agent_plugin["binaries"] == {"linux": plugin_dict["binaries"]["linux"]}
    assert mongo_client.monkey_island.agent_plugins_binaries_linux.files.count_documents({}) == 1
    assert mongo_client.monkey_island.agent_plugins_binaries_windows.files.count_documents({}) == 0


def test_remove_agent_plugin__no_error_if_plugin_does_not_exist(
    agent_plugin_repository,
):
    agent_plugin_repository.remove_agent_plugin(
        AgentPluginType.EXPLOITER, EXPLOITER_NAME_1, OperatingSystem.WINDOWS
    )


def test_remove_agent_plugin__removalerror_if_problem_deleting_plugin(
    plugin_file, insert_plugin, mongo_client, agent_plugin_repository
):
    with open(plugin_file, "rb") as file:
        plugin_dict = insert_plugin(file, OperatingSystem.WINDOWS)
    mongo_client.monkey_island.agent_plugins.find_one = MagicMock(return_value=plugin_dict)
    mongo_client.monkey_island.agent_plugins.delete_one = MagicMock(side_effect=Exception("foo"))

    with pytest.raises(RemovalError):
        agent_plugin_repository.remove_agent_plugin(
            AgentPluginType.EXPLOITER, EXPLOITER_NAME_1, OperatingSystem.WINDOWS
        )


def test_remove_agent_plugin__removalerror_if_problem_updating_plugin(
    plugin_file, insert_plugin, mongo_client, agent_plugin_repository
):
    with open(plugin_file, "rb") as file:
        plugin_dict = insert_plugin(file, OperatingSystem.WINDOWS)
        plugin_dict = insert_plugin(file, OperatingSystem.LINUX, plugin_dict)
    mongo_client.monkey_island.agent_plugins.find_one = MagicMock(return_value=plugin_dict)
    mongo_client.monkey_island.agent_plugins.update_one = MagicMock(side_effect=Exception("foo"))

    with pytest.raises(RemovalError):
        agent_plugin_repository.remove_agent_plugin(
            AgentPluginType.EXPLOITER, EXPLOITER_NAME_1, OperatingSystem.WINDOWS
        )


def test_remove_agent_plugin__removalerror_if_problem_deleting_binary(
    plugin_file, insert_plugin, mongo_client, agent_plugin_repository
):
    with open(plugin_file, "rb") as file:
        plugin_dict = insert_plugin(file, OperatingSystem.WINDOWS)
        plugin_dict = insert_plugin(file, OperatingSystem.LINUX, plugin_dict)
    mongo_client.monkey_island.agent_plugins.find_one = MagicMock(return_value=plugin_dict)
    mongo_client.monkey_island.agent_plugins_binaries_windows.files.delete_one = MagicMock(
        side_effect=Exception("foo")
    )

    with pytest.raises(RemovalError):
        agent_plugin_repository.remove_agent_plugin(
            AgentPluginType.EXPLOITER, EXPLOITER_NAME_1, OperatingSystem.WINDOWS
        )
