import tarfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from common.agent_plugins import AgentPluginType
from infection_monkey.i_puppet import UnknownPluginError
from infection_monkey.island_api_client import (
    IslandAPIConnectionError,
    IslandAPIRequestError,
    IslandAPIRequestFailedError,
    IslandAPITimeoutError,
)
from infection_monkey.master.plugin_registry import PluginRegistry, check_safe_archive


@pytest.fixture
def bad_tar_file(plugin_data_dir) -> tarfile.TarFile:
    return tarfile.open(plugin_data_dir / "zip_slip.tar")


@pytest.fixture
def good_tar_file(plugin_data_dir) -> tarfile.TarFile:
    return tarfile.open(plugin_data_dir / "test-exploiter.tar")


@pytest.mark.parametrize("path", [Path("/home/user"), Path("/home/user/plugins")])
def test_check_safe_archive__false_if_unsafe(path, bad_tar_file):
    assert check_safe_archive(path, bad_tar_file) is False


def test_check_safe_archive__true_if_root_dir(bad_tar_file):
    assert check_safe_archive(Path("/"), bad_tar_file) is True


@pytest.mark.parametrize("path", [Path("/home/user"), Path("/home/user/plugins")])
def test_check_safe_archive__true_if_safe(path, good_tar_file):
    assert check_safe_archive(path, good_tar_file) is True


@pytest.fixture
def island_api_client():
    return MagicMock()


@pytest.fixture
def plugin_loader():
    return MagicMock()


def test_get_plugin_not_found(island_api_client, plugin_loader, tmp_path):
    island_api_client.get_agent_plugin = MagicMock(side_effect=IslandAPIRequestError)
    plugin_registry = PluginRegistry(island_api_client, plugin_loader, tmp_path)

    with pytest.raises(UnknownPluginError):
        plugin_registry.get_plugin("Ghost", AgentPluginType.PAYLOAD)


@pytest.mark.parametrize(
    "error", [IslandAPIConnectionError, IslandAPIRequestFailedError, IslandAPITimeoutError]
)
def test_get_plugin_unexpected_response(error, island_api_client, plugin_loader, tmp_path):
    island_api_client.get_agent_plugin = MagicMock(side_effect=error)
    plugin_registry = PluginRegistry(island_api_client, plugin_loader, tmp_path)

    with pytest.raises(Exception):
        plugin_registry.get_plugin("Ghost", AgentPluginType.PAYLOAD)
