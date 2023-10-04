from monkeytypes import AgentPluginManifest, AgentPluginType, OperatingSystem

from common.agent_plugins import PluginName

# For `AgentPluginManifest.version`, mypy complains even if you
# pass it a `PluginVersion` object, so we're ignoring the error.
HARD_CODED_FINGERPRINTER_MANIFESTS = {
    "smb": AgentPluginManifest(
        name=PluginName("smb"),
        plugin_type=AgentPluginType.FINGERPRINTER,
        supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        target_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        title="SMB Fingerprinter",
        version="1.0.0",  # type: ignore [arg-type]
        description="Figures out if SMB is running and what's the version of it.",
        safe=True,
    ),
    "ssh": AgentPluginManifest(
        name=PluginName("ssh"),
        plugin_type=AgentPluginType.FINGERPRINTER,
        supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        target_operating_systems=(OperatingSystem.LINUX,),
        title="SSH Fingerprinter",
        version="1.0.0",  # type: ignore [arg-type]
        description="Figures out if SSH is running.",
        safe=True,
    ),
    "http": AgentPluginManifest(
        name=PluginName("http"),
        plugin_type=AgentPluginType.FINGERPRINTER,
        supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        target_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        title="HTTP Fingerprinter",
        version="1.0.0",  # type: ignore [arg-type]
        description="Checks if host has HTTP/HTTPS ports open.",
        safe=True,
    ),
    "mssql": AgentPluginManifest(
        name=PluginName("mssql"),
        plugin_type=AgentPluginType.FINGERPRINTER,
        supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        target_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        title="MSSQL Fingerprinter",
        version="1.0.0",  # type: ignore [arg-type]
        description="Checks if Microsoft SQL service is running and tries to gather "
        "information about it.",
        safe=True,
    ),
}
