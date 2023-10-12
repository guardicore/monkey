from base64 import b64encode
from typing import Any, Dict, Tuple

from monkeytypes import AgentPluginManifest, B64Bytes, InfectionMonkeyBaseModel, OperatingSystem
from pydantic import field_serializer


class AgentPlugin(InfectionMonkeyBaseModel):
    """
    Class describing agent plugin

    Attributes:
        :param plugin_manifest: Metadata describing the plugin
        :param config_schema: JSONSchema describing the configuration options
        :param source_archive: Contents of the plugin codebase
        :param supported_operating_systems: Operating systems on which the plugin can run
    """

    plugin_manifest: AgentPluginManifest
    # Should be JSONSerializable but it's only supported in 3.9:
    # https://github.com/pydantic/pydantic/pull/1844
    config_schema: Dict[str, Any]
    source_archive: B64Bytes
    supported_operating_systems: Tuple[OperatingSystem, ...]

    @field_serializer("source_archive", when_used="json")
    def dump_source_archive(self, v):
        return b64encode(v).decode()
