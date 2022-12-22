import copy
from typing import Any, Dict

from common import OperatingSystem
from common.agent_plugins.agent_plugin_manifest import AgentPluginManifest
from common.agent_plugins.agent_plugin_type import AgentPluginType

FAKE_NAME = "rdp_exploiter"
FAKE_NAME2 = "ssh_exploiter"
FAKE_TYPE = "Exploiter"
FAKE_OPERATING_SYSTEMS = ["linux"]
FAKE_TITLE = "Remote Desktop Protocol exploiter"
FAKE_LINK = "www.beefface.com"

FAKE_AGENT_MANIFEST_DICT_IN: Dict[str, Any] = {
    "name": FAKE_NAME,
    "plugin_type": FAKE_TYPE,
    "supported_operating_systems": FAKE_OPERATING_SYSTEMS,
    "title": FAKE_TITLE,
    "link_to_documentation": FAKE_LINK,
}

FAKE_AGENT_MANIFEST_DICT_OUT: Dict[str, Any] = copy.deepcopy(FAKE_AGENT_MANIFEST_DICT_IN)
FAKE_AGENT_MANIFEST_DICT_OUT["description"] = None
FAKE_AGENT_MANIFEST_DICT_OUT["safe"] = False

FAKE_AGENT_MANIFEST_DICT = {
    "name": FAKE_NAME,
    "plugin_type": AgentPluginType.EXPLOITER,
    "supported_operating_systems": [OperatingSystem.LINUX],
    "title": FAKE_TITLE,
    "link_to_documentation": FAKE_LINK,
}

FAKE_MANIFEST_OBJECT = AgentPluginManifest(
    name=FAKE_NAME,
    plugin_type=FAKE_TYPE,
    supported_operating_systems=FAKE_OPERATING_SYSTEMS,
    title=FAKE_TITLE,
    link_to_documentation=FAKE_LINK,
)


def test_agent_plugin_manifest__serialization():
    assert FAKE_MANIFEST_OBJECT.dict(simplify=True) == FAKE_AGENT_MANIFEST_DICT_OUT


def test_agent_plugin_manifest__deserialization():
    assert AgentPluginManifest(**FAKE_AGENT_MANIFEST_DICT_IN) == FAKE_MANIFEST_OBJECT
