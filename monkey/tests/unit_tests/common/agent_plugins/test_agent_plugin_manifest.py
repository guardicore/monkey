import copy
from typing import Any, Dict

import pytest

from common import OperatingSystem
from common.agent_plugins.agent_plugin_manifest import AgentPluginManifest
from common.agent_plugins.agent_plugin_type import AgentPluginType

FAKE_NAME = "rdp_exploiter"
FAKE_NAME2 = "ssh_exploiter"
FAKE_TYPE = "Exploiter"
FAKE_OPERATING_SYSTEMS = ["linux"]
FAKE_SUPPORTED_OPERATING_SYSTEMS = ["linux", "windows"]
FAKE_TITLE = "Remote Desktop Protocol exploiter"
FAKE_LINK = "www.beefface.com"

FAKE_AGENT_MANIFEST_DICT_IN: Dict[str, Any] = {
    "name": FAKE_NAME,
    "plugin_type": FAKE_TYPE,
    "supported_operating_systems": FAKE_SUPPORTED_OPERATING_SYSTEMS,
    "target_operating_systems": FAKE_OPERATING_SYSTEMS,
    "title": FAKE_TITLE,
    "link_to_documentation": FAKE_LINK,
}

FAKE_AGENT_MANIFEST_DICT_OUT: Dict[str, Any] = copy.deepcopy(FAKE_AGENT_MANIFEST_DICT_IN)
FAKE_AGENT_MANIFEST_DICT_OUT["description"] = None
FAKE_AGENT_MANIFEST_DICT_OUT["safe"] = False
FAKE_AGENT_MANIFEST_DICT_OUT["remediation_suggestion"] = None

FAKE_AGENT_MANIFEST_DICT = {
    "name": FAKE_NAME,
    "plugin_type": AgentPluginType.EXPLOITER,
    "supported_operating_systems": [OperatingSystem.LINUX, OperatingSystem.WINDOWS],
    "target_operating_systems": [OperatingSystem.LINUX],
    "title": FAKE_TITLE,
    "link_to_documentation": FAKE_LINK,
}

FAKE_MANIFEST_OBJECT = AgentPluginManifest(
    name=FAKE_NAME,
    plugin_type=FAKE_TYPE,
    supported_operating_systems=FAKE_SUPPORTED_OPERATING_SYSTEMS,
    target_operating_systems=FAKE_OPERATING_SYSTEMS,
    title=FAKE_TITLE,
    link_to_documentation=FAKE_LINK,
)


def test_agent_plugin_manifest__serialization():
    assert FAKE_MANIFEST_OBJECT.dict(simplify=True) == FAKE_AGENT_MANIFEST_DICT_OUT


def test_agent_plugin_manifest__deserialization():
    assert AgentPluginManifest(**FAKE_AGENT_MANIFEST_DICT_IN) == FAKE_MANIFEST_OBJECT


@pytest.mark.parametrize(
    "name",
    [
        "../../test_dir12341234",
        "/test_dir12341234",
        "test_dir/../../../12341234",
        "../../../",
        "..",
        ".",
        "$HOME",
        "~/",
        "!!",
        "!#",
        "!$",
        "name with spaces",
        "name; malicious command",
        "`shell_injection`",
        "$(shell_injection)",
        "bash -c shell_injection",
    ],
)
def test_agent_plugin_manifest__invalid_name(name):
    with pytest.raises(ValueError):
        AgentPluginManifest(
            name=name,
            plugin_type=FAKE_TYPE,
            supported_operating_systems=FAKE_SUPPORTED_OPERATING_SYSTEMS,
            target_operating_systems=FAKE_OPERATING_SYSTEMS,
            title=FAKE_TITLE,
            link_to_documentation=FAKE_LINK,
        )


def test_agent_plugin_manifest__remediation_suggestion():
    remediation_suggestion = "test remediation suggestion"
    agent_manifest_dict = FAKE_AGENT_MANIFEST_DICT.copy()
    agent_manifest_dict["remediation_suggestion"] = remediation_suggestion

    agent_manifest_object = AgentPluginManifest(**agent_manifest_dict)

    assert agent_manifest_object.remediation_suggestion == remediation_suggestion
