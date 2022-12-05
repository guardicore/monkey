import copy
from typing import Any, Dict

from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import (
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

# TODO fix byte serialization, this should be bytes
FAKE_ZEROLOGON_PLUGIN_ARCHIVE = "fake archive"

FAKE_AGENT_PLUGIN_DICT_IN: Dict[str, Any] = {
    "plugin_manifest": FAKE_AGENT_MANIFEST_DICT_IN,
    "config_schema": FAKE_ZEROLOGON_PLUGIN_CONFIG_SCHEMA,
    "default_config": FAKE_ZEROLOGON_PLUGIN_CONFIG,
    "source_archive": FAKE_ZEROLOGON_PLUGIN_ARCHIVE,
}

FAKE_AGENT_PLUGIN_DICT_OUT = copy.deepcopy(FAKE_AGENT_PLUGIN_DICT_IN)
FAKE_AGENT_PLUGIN_DICT_OUT["plugin_manifest"] = FAKE_AGENT_MANIFEST_DICT_OUT

FAKE_AGENT_PLUGIN_OBJECT = AgentPlugin(
    plugin_manifest=FAKE_MANIFEST_OBJECT,
    config_schema=FAKE_ZEROLOGON_PLUGIN_CONFIG_SCHEMA,
    default_config=FAKE_ZEROLOGON_PLUGIN_CONFIG,
    source_archive=FAKE_ZEROLOGON_PLUGIN_ARCHIVE,
)


def test_agent_plugin_serialization():
    assert FAKE_AGENT_PLUGIN_OBJECT.dict(simplify=True) == FAKE_AGENT_PLUGIN_DICT_OUT


def test_agent_plugin_deserialization():
    assert AgentPlugin(**FAKE_AGENT_PLUGIN_DICT_IN) == FAKE_AGENT_PLUGIN_OBJECT
