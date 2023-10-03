from monkeytypes import AgentPluginManifest
from tests.common.fake_manifests import FAKE_MANIFEST_OBJECT, FAKE_NAME2

from common import OperatingSystem
from common.agent_plugins import AgentPlugin

FAKE_PLUGIN_CONFIG_SCHEMA_1 = {
    "title": "Mock exploiter",
    "description": "Configuration settings for Mock exploiter.",
    "type": "object",
    "required": ["exploitation_success_rate", "propagation_success_rate"],
    "properties": {
        "exploitation_success_rate": {
            "title": "Exploitation success rate",
            "description": "The rate of successful exploitation in percentage",
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "default": 50,
        },
        "propagation_success_rate": {
            "title": "Propagation success rate",
            "description": "The rate of successful propagation in percentage",
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "default": 50,
        },
    },
}

FAKE_PLUGIN_ARCHIVE_1 = b"random bytes"

FAKE_AGENT_PLUGIN_1 = AgentPlugin(
    plugin_manifest=FAKE_MANIFEST_OBJECT,
    config_schema=FAKE_PLUGIN_CONFIG_SCHEMA_1,
    source_archive=FAKE_PLUGIN_ARCHIVE_1,
    supported_operating_systems=(OperatingSystem.LINUX,),
)


FAKE_PLUGIN_CONFIG_SCHEMA_2 = {
    "title": "Mock exploiter",
    "description": "Configuration settings for Mock exploiter.",
    "type": "object",
    "required": ["timeout"],
    "properties": {
        "timeout": {
            "title": "Timeout",
            "description": "How long the exploiter should run for",
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "default": 50,
        }
    },
}

FAKE_PLUGIN_ARCHIVE_2 = b"other random bytes"

_manifest_params = FAKE_MANIFEST_OBJECT.dict(simplify=True)
_manifest_params["name"] = FAKE_NAME2

FAKE_AGENT_PLUGIN_2 = AgentPlugin(
    plugin_manifest=AgentPluginManifest(**_manifest_params),
    config_schema=FAKE_PLUGIN_CONFIG_SCHEMA_2,
    source_archive=FAKE_PLUGIN_ARCHIVE_2,
    supported_operating_systems=(OperatingSystem.WINDOWS,),
)
