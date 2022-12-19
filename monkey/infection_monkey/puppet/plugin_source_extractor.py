import io
from pathlib import Path
from tarfile import TarFile

from common.agent_plugins import AgentPlugin
from common.utils.file_utils import create_secure_directory


class PluginSourceExtractor:
    def __init__(self, plugin_directory: Path):
        self._plugin_directory = plugin_directory

    # TODO: This function contains security vulnerabilities. Fix it.
    def extract_plugin_source(self, agent_plugin: AgentPlugin):
        destination = self.plugin_directory / agent_plugin.plugin_manifest.name
        create_secure_directory(destination)
        archive = TarFile(fileobj=io.BytesIO(agent_plugin.source_archive), mode="r")
        archive.extractall(destination)

    @property
    def plugin_directory(self) -> Path:
        return self._plugin_directory
