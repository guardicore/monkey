import logging
from pathlib import Path

from common import DIContainer
from monkey_island.cc.services.agent_plugin_service import IAgentPluginService
from monkey_island.cc.services.agent_plugin_service.errors import PluginInstallationError

from .data_dir import PLUGIN_DIR_NAME

logger = logging.getLogger(__name__)


def install_plugins(container: DIContainer, data_dir: Path):
    agent_plugin_service = container.resolve(IAgentPluginService)

    plugins_dir = data_dir / PLUGIN_DIR_NAME
    plugin_tar_file_paths = list(plugins_dir.glob("*.tar"))

    for path in plugin_tar_file_paths:
        with open(path, "rb") as f:
            plugin_archive = f.read()
            try:
                agent_plugin_service.install_plugin_archive(plugin_archive)
            except PluginInstallationError:
                logger.warning(f"Failed to install plugin at {path}")
