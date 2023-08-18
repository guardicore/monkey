from pathlib import Path
from typing import BinaryIO, Callable
from unittest.mock import MagicMock

import pytest

from common import OperatingSystem
from monkey_island.cc.services.agent_plugin_service.agent_plugin_service import AgentPluginService
from monkey_island.cc.services.agent_plugin_service.i_agent_plugin_repository import (
    IAgentPluginRepository,
)
from monkey_island.cc.services.agent_plugin_service.i_agent_plugin_service import (
    IAgentPluginService,
)


@pytest.fixture
def agent_plugin_repository() -> IAgentPluginRepository:
    return MagicMock(spec=IAgentPluginRepository)


@pytest.fixture
def agent_plugin_service(agent_plugin_repository) -> IAgentPluginService:
    return AgentPluginService(agent_plugin_repository)


@pytest.mark.parametrize(
    "plugin_os, plugin_path",
    [
        (OperatingSystem.WINDOWS, "only-windows-vendor-plugin-source-input.tar"),
        (OperatingSystem.LINUX, "only-linux-vendor-plugin-source-input.tar"),
    ],
)
def test_agent_plugin_service__install_agent_plugin_archive(
    plugin_data_dir: Path,
    plugin_os: OperatingSystem,
    plugin_path: str,
    agent_plugin_repository: IAgentPluginRepository,
    agent_plugin_service: IAgentPluginService,
    build_agent_plugin_tar_with_source_tar: Callable[[Path], BinaryIO],
):
    agent_plugin_tar = build_agent_plugin_tar_with_source_tar(plugin_data_dir / plugin_path)
    agent_plugin_service.install_agent_plugin_archive(agent_plugin_tar.getvalue())

    assert agent_plugin_repository.remove_agent_plugin.call_count == 1
    assert agent_plugin_repository.remove_agent_plugin.call_args[1]["operating_system"] is None

    assert agent_plugin_repository.store_agent_plugin.call_count == 1
    assert agent_plugin_repository.store_agent_plugin.call_args[1]["operating_system"] is plugin_os


@pytest.mark.parametrize(
    "plugin_path_actual",
    ["multi-vendor-plugin-source-input.tar", "cross-platform-plugin-source.tar"],
)
def test_agent_plugin_service__install_agent_plugin_archive_multi(
    plugin_data_dir: Path,
    plugin_path_actual: str,
    agent_plugin_repository: IAgentPluginRepository,
    agent_plugin_service: IAgentPluginService,
    build_agent_plugin_tar_with_source_tar: Callable[[Path], BinaryIO],
):
    agent_plugin_tar = build_agent_plugin_tar_with_source_tar(plugin_data_dir / plugin_path_actual)
    agent_plugin_service.install_agent_plugin_archive(agent_plugin_tar.getvalue())

    assert agent_plugin_repository.remove_agent_plugin.call_count == 1
    assert agent_plugin_repository.remove_agent_plugin.call_args[1]["operating_system"] is None
    assert agent_plugin_repository.store_agent_plugin.call_count == 2
