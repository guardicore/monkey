from common.agent_plugins import AgentPluginManifest, AgentPluginType, PluginName
from common.operating_system import OperatingSystem

HARD_CODED_FINGERPRINTER_MANIFESTS = {
    "smb": AgentPluginManifest(
        name=PluginName("smb"),
        plugin_type=AgentPluginType.FINGERPRINTER,
        supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        target_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        title="SMB Fingerprinter",
        version="1.0.0",  # type: ignore [arg-type]
        description="Figures out if SMB is running and what's the version of it.",
        remediation_suggestion=None,
        link_to_documentation=None,
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
        remediation_suggestion=None,
        link_to_documentation=None,
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
        remediation_suggestion=None,
        link_to_documentation=None,
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
        remediation_suggestion=None,
        link_to_documentation=None,
        safe=True,
    ),
}
