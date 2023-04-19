from common.agent_plugins import AgentPluginManifest, AgentPluginType
from common.operating_system import OperatingSystem

HARD_CODED_PAYLOADS_MANIFESTS = {
    "ransomware": AgentPluginManifest(
        name="ransomware",
        plugin_type=AgentPluginType.PAYLOAD,
        supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        target_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
        title="Ransomware Simulation",
        version="1.0.0",
        description="To simulate ransomware encryption, you'll need to provide Infection Monkey "
        "with files that it can safely encrypt. Create a directory with some files on each "
        "machine where the ransomware simulation will run."
        "\n\nNo files will be encrypted if a directory is not specified or if the specified "
        "directory doesn't exist on a victim machine. "
        "Note that a README.txt will be left in the specified target directory.",
    )
}
