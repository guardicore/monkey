import copy
from typing import Any

from monkeytypes import AgentPluginManifest, AgentPluginType, OperatingSystem

FAKE_NAME = "rdp_exploiter"
FAKE_NAME2 = "ssh_exploiter"
FAKE_TYPE = "Exploiter"
FAKE_OPERATING_SYSTEMS = ["linux"]
FAKE_SUPPORTED_OPERATING_SYSTEMS = ["linux", "windows"]
FAKE_TITLE = "Remote Desktop Protocol exploiter"
URL = "http://www.beefface.com/"

FAKE_AGENT_MANIFEST_DICT_IN: dict[str, Any] = {
    "name": FAKE_NAME,
    "plugin_type": FAKE_TYPE,
    "supported_operating_systems": FAKE_SUPPORTED_OPERATING_SYSTEMS,
    "target_operating_systems": FAKE_OPERATING_SYSTEMS,
    "title": FAKE_TITLE,
    "version": "1.0.0",
    "link_to_documentation": URL,
}

FAKE_AGENT_MANIFEST_DICT_OUT: dict[str, Any] = copy.deepcopy(FAKE_AGENT_MANIFEST_DICT_IN)
FAKE_AGENT_MANIFEST_DICT_OUT["description"] = None
FAKE_AGENT_MANIFEST_DICT_OUT["safe"] = False
FAKE_AGENT_MANIFEST_DICT_OUT["remediation_suggestion"] = None

FAKE_AGENT_MANIFEST_DICT = {
    "name": FAKE_NAME,
    "plugin_type": AgentPluginType.EXPLOITER,
    "supported_operating_systems": [OperatingSystem.LINUX, OperatingSystem.WINDOWS],
    "target_operating_systems": [OperatingSystem.LINUX],
    "title": FAKE_TITLE,
    "version": "1.0.0",
    "link_to_documentation": URL,
}

FAKE_MANIFEST_OBJECT = AgentPluginManifest(
    name=FAKE_NAME,
    plugin_type=FAKE_TYPE,
    supported_operating_systems=FAKE_SUPPORTED_OPERATING_SYSTEMS,
    target_operating_systems=FAKE_OPERATING_SYSTEMS,
    title=FAKE_TITLE,
    version="1.0.0",
    link_to_documentation=URL,
)
