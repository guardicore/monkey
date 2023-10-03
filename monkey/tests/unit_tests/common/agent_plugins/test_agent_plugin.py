import copy
from base64 import b64encode
from typing import Any, Dict

from monkeytypes import OperatingSystem
from tests.common.fake_manifests import (
    FAKE_AGENT_MANIFEST_DICT_IN,
    FAKE_AGENT_MANIFEST_DICT_OUT,
    FAKE_MANIFEST_OBJECT,
)

from common.agent_plugins.agent_plugin import AgentPlugin

FAKE_ZEROLOGON_PLUGIN_CONFIG_SCHEMA = {
    "plugin_options": {
        "type": "object",
        "title": "Zerologon options",
        "properties": {
            "attempt_count": {
                "type": "number",
                "title": "attempt count",
                "description": "how many attempts to do to change the password",
            },
            "password_to_set": {
                "type": "string",
                "title": "password to set",
                "description": "zero logon will change the password. Select what to change it to",
            },
            "dc_ip_address": {
                "type": "string",
                "title": "IP of a domain controller",
                "format": "ipv4",
                "description": "Zerologon will exploit a domain controller, so provide its IP",
            },
        },
    }
}

FAKE_ZEROLOGON_PLUGIN_CONFIG = {
    "attempt_count": 2000,
    "password_to_set": "SeCuRe",
    "dc_ip_address": "localhost",
}

FAKE_ZEROLOGON_PLUGIN_ARCHIVE = b"random bytes"

FAKE_ZEROLOGON_HOST_OS = (OperatingSystem.LINUX, OperatingSystem.WINDOWS)

FAKE_AGENT_PLUGIN_DICT_IN: Dict[str, Any] = {
    "plugin_manifest": FAKE_AGENT_MANIFEST_DICT_IN,
    "config_schema": FAKE_ZEROLOGON_PLUGIN_CONFIG_SCHEMA,
    "source_archive": FAKE_ZEROLOGON_PLUGIN_ARCHIVE,
    "supported_operating_systems": FAKE_ZEROLOGON_HOST_OS,
}

FAKE_AGENT_PLUGIN_DICT_OUT = copy.deepcopy(FAKE_AGENT_PLUGIN_DICT_IN)
FAKE_AGENT_PLUGIN_DICT_OUT["plugin_manifest"] = FAKE_AGENT_MANIFEST_DICT_OUT
FAKE_AGENT_PLUGIN_DICT_OUT["source_archive"] = b64encode(FAKE_ZEROLOGON_PLUGIN_ARCHIVE).decode()
FAKE_AGENT_PLUGIN_DICT_OUT["supported_operating_systems"] = [
    FAKE_ZEROLOGON_HOST_OS[0].value,
    FAKE_ZEROLOGON_HOST_OS[1].value,
]

FAKE_AGENT_PLUGIN_OBJECT = AgentPlugin(
    plugin_manifest=FAKE_MANIFEST_OBJECT,
    config_schema=FAKE_ZEROLOGON_PLUGIN_CONFIG_SCHEMA,
    source_archive=FAKE_ZEROLOGON_PLUGIN_ARCHIVE,
    supported_operating_systems=FAKE_ZEROLOGON_HOST_OS,
)


def test_agent_plugin__serialization():
    assert FAKE_AGENT_PLUGIN_OBJECT.dict(simplify=True) == FAKE_AGENT_PLUGIN_DICT_OUT


def test_agent_plugin__full_serialization():
    assert AgentPlugin(**FAKE_AGENT_PLUGIN_OBJECT.dict(simplify=True)) == FAKE_AGENT_PLUGIN_OBJECT


def test_agent_plugin__deserialization():
    assert AgentPlugin(**FAKE_AGENT_PLUGIN_DICT_IN) == FAKE_AGENT_PLUGIN_OBJECT
