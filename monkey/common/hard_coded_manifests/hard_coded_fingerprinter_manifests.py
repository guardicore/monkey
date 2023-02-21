from common.agent_plugins import AgentPluginManifest, AgentPluginType
from common.operating_system import OperatingSystem

HARD_CODED_EXPLOITER_MANIFESTS = {
    "smb": AgentPluginManifest(
        name="smb",
        plugin_type=AgentPluginType.FINGERPRINTER,
        supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        target_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        title="SMB Fingerprinter",
        version="1.0.0",
        description="Figures out if SMB is running " "and what's the version of it.",
        safe=True,
    ),
    "ssh": AgentPluginManifest(
        name="ssh",
        plugin_type=AgentPluginType.FINGERPRINTER,
        supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        target_operating_systems=(OperatingSystem.LINUX,),
        title="SSH Fingerprinter",
        version="1.0.0",
        description="Figures out if SSH is running.",
        safe=True,
    ),
    "http": AgentPluginManifest(
        name="http",
        plugin_type=AgentPluginType.FINGERPRINTER,
        supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        target_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        title="HTTP Fingerprinter",
        version="1.0.0",
        description="Checks if host has HTTP/HTTPS ports open.",
        safe=True,
    ),
    "mssql": AgentPluginManifest(
        name="mssql",
        plugin_type=AgentPluginType.FINGERPRINTER,
        supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        target_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        title="HTTP Fingerprinter",
        version="1.0.0",
        description="Checks if host has HTTP/HTTPS ports open.",
        safe=True,
    ),
}
