from base64 import b64encode
from typing import Any, Callable, Dict, Mapping, Tuple, Type

from monkeytypes import (
    AgentPluginManifest,
    InfectionMonkeyBaseModel,
    InfectionMonkeyModelConfig,
    OperatingSystem,
)

from common.types import B64Bytes


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

    class Config(InfectionMonkeyModelConfig):
        # b64encode() returns bytes, so we call decode() to transform bytes to str
        # Pydantic is not able to inherit AgentPluginManifest json encoders
        # so we update the current encoders
        json_encoders: Mapping[Type, Callable[[Any], Any]] = {
            bytes: lambda byte_field: b64encode(byte_field).decode(),
            **AgentPluginManifest.Config.json_encoders,
        }
