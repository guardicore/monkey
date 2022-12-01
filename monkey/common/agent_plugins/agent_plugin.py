from common.types import JSONSerializable

from .plugin_manifest import AgentPluginManifest


class AgentPlugin:
    plugin_manifest: AgentPluginManifest
    config_schema: JSONSerializable
    default_config: JSONSerializable
    source_archive: bytes
