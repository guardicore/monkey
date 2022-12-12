from tests.unit_tests.common.agent_plugins.test_agent_plugin_manifest import FAKE_MANIFEST_OBJECT

from common.agent_plugins import AgentPlugin

FAKE_PLUGIN_CONFIG_SCHEMA_1 = {"plugin_options": {"some_option": "some_value"}}

FAKE_PLUGIN_ARCHIVE_1 = b"random bytes"

FAKE_AGENT_PLUGIN_1 = AgentPlugin(
    plugin_manifest=FAKE_MANIFEST_OBJECT,
    config_schema=FAKE_PLUGIN_CONFIG_SCHEMA_1,
    source_archive=FAKE_PLUGIN_ARCHIVE_1,
)


FAKE_PLUGIN_CONFIG_SCHEMA_2 = {"plugin_options": {"other_option": "other_value"}}

FAKE_PLUGIN_ARCHIVE_2 = b"other random bytes"

FAKE_AGENT_PLUGIN_2 = AgentPlugin(
    plugin_manifest=FAKE_MANIFEST_OBJECT,
    config_schema=FAKE_PLUGIN_CONFIG_SCHEMA_2,
    source_archive=FAKE_PLUGIN_ARCHIVE_2,
)
