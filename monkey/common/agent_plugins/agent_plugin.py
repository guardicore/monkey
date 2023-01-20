from base64 import b64encode
from typing import Any, Dict, Tuple

from common import OperatingSystem
from common.agent_plugins import AgentPluginManifest
from common.base_models import InfectionMonkeyBaseModel
from common.types.b64_bytes import B64Bytes


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

    class Config:
        # b64encode() returns bytes, so we call decode() to transform bytes to str
        json_encoders = {bytes: lambda byte_field: b64encode(byte_field).decode()}
