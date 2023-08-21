import gridfs
import mongomock
import pytest
from mongomock.gridfs import enable_gridfs_integration
from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import FAKE_NAME
from tests.unit_tests.monkey_island.cc.fake_agent_plugin_data import FAKE_AGENT_PLUGIN_1

from common import OperatingSystem
from common.agent_plugins import AgentPluginManifest, AgentPluginType
from monkey_island.cc.repositories import UnknownRecordError
from monkey_island.cc.services.agent_plugin_service.mongo_agent_plugin_repository import (
    MongoAgentPluginRepository,
)

enable_gridfs_integration()


EXPECTED_MANIFEST = AgentPluginManifest(
    name="test",
    plugin_type=AgentPluginType.EXPLOITER,
    supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
    target_operating_systems=(OperatingSystem.WINDOWS, OperatingSystem.LINUX),
    title="dummy-exploiter",
    version="1.0.0",
    description="A dummy exploiter",
    safe=True,
)


@pytest.fixture
def mongo_client():
    client = mongomock.MongoClient()

    return client


@pytest.fixture
def insert_plugin(mongo_client):
    def impl(file, operating_system: OperatingSystem):
        binaries_collection = gridfs.GridFS(
            mongo_client.monkey_island, f"agent_plugins_binaries_{operating_system.value}"
        )
        id = binaries_collection.put(file)
        plugin_dict = {
            "plugin_manifest": {
                "name": "test",
                "plugin_type": "Exploiter",
                "supported_operating_systems": ["linux", "windows"],
                "target_operating_systems": ["windows", "linux"],
                "title": "dummy-exploiter",
                "version": "1.0.0",
                "description": "A dummy exploiter",
                "safe": True,
            },
            "config_schema": {},
            "binaries": {f"{operating_system.value}": id},
            "supported_operating_systems": ("windows",),
        }
        mongo_client.monkey_island.agent_plugins.insert_one(plugin_dict)

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
        OperatingSystem.WINDOWS, AgentPluginType.EXPLOITER, "test"
    )

    assert plugin.plugin_manifest == EXPECTED_MANIFEST
    assert isinstance(plugin.config_schema, dict)
    assert len(plugin.source_archive) == 10240


def test_get_plugin__UnknownRecordError_if_not_exist(agent_plugin_repository):
    with pytest.raises(UnknownRecordError):
        agent_plugin_repository.get_plugin(
            OperatingSystem.WINDOWS, AgentPluginType.EXPLOITER, "does_not_exist"
        )


# def test_get_plugin__RetrievalError_if_bad_plugin(
#     bad_plugin_file, mongo_client, agent_plugin_repository: MongoAgentPluginRepository
# ):
#     with open(bad_plugin_file, "rb") as file:
#         file_repository.save_file(basename(bad_plugin_file), file)
#     with pytest.raises(RetrievalError):
#         agent_plugin_repository.get_plugin(
#             OperatingSystem.WINDOWS, AgentPluginType.EXPLOITER, "bad"
#         )


# def test_get_plugin__RetrievalError_if_unsupported_os(
#     plugin_file, mongo_client, agent_plugin_repository: MongoAgentPluginRepository
# ):
#     with open(plugin_file, "rb") as file:
#         file_repository.save_file(basename(plugin_file), file)
#     with pytest.raises(RetrievalError):
#         agent_plugin_repository.get_plugin("unrecognised OS", AgentPluginType.EXPLOITER, "test")


# def test_get_all_plugin_manifests(
#     plugin_file, file_repository: InMemoryFileRepository, agent_plugin_repository
# ):
#     with open(plugin_file, "rb") as file:
#         file_repository.save_file(basename(plugin_file), file)

#     actual_plugin_manifests = agent_plugin_repository.get_all_plugin_manifests()

#     assert actual_plugin_manifests == {AgentPluginType.EXPLOITER: {"test": EXPECTED_MANIFEST}}


# def test_get_all_plugin_manifests__RetrievalError_if_bad_plugin_type(
#     plugin_file, file_repository: InMemoryFileRepository, agent_plugin_repository
# ):
#     with open(plugin_file, "rb") as file:
#         file_repository.save_file("ssh-bogus.tar", file)

#     with pytest.raises(RetrievalError):
#         agent_plugin_repository.get_all_plugin_manifests()


def test_store_agent_plugin(agent_plugin_repository: MongoAgentPluginRepository):
    agent_plugin_repository.store_agent_plugin(OperatingSystem.LINUX, FAKE_AGENT_PLUGIN_1)

    plugin = agent_plugin_repository.get_plugin(
        OperatingSystem.LINUX, AgentPluginType.EXPLOITER, FAKE_NAME
    )
    assert plugin == FAKE_AGENT_PLUGIN_1


# def test_remove_agent_plugin():
#     pass
