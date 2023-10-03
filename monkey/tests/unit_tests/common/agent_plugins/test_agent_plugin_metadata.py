from monkeytypes import AgentPluginType

from common.agent_plugins import AgentPluginMetadata

from .test_agent_plugin_repository_index import PAYLOAD_PLUGIN_NAME, PLUGIN_VERSION_1_2_3

PLUGIN_VERSION_1_2_3_SERIALIZED = {
    "name": PAYLOAD_PLUGIN_NAME,
    "plugin_type": AgentPluginType.PAYLOAD.value,
    "resource_path": "/tmp",
    "sha256": "7ac0f5c62a9bcb81af3e9d67a764d7bbd3cce9af7cd26c211f136400ebe703c4",
    "description": "an awesome payload plugin",
    "version": "1.2.3",
    "safe": True,
}


def test_agent_plugin_metadata_serialization():
    assert PLUGIN_VERSION_1_2_3.dict(simplify=True) == PLUGIN_VERSION_1_2_3_SERIALIZED


def test_agent_plugin_metadata_deserialization():
    assert AgentPluginMetadata(**PLUGIN_VERSION_1_2_3_SERIALIZED) == PLUGIN_VERSION_1_2_3
