import tarfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from flask import Response

from common.agent_plugins import AgentPluginType
from infection_monkey.i_puppet import UnknownPluginError
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


class StubIslandAPIClient:
    def __init__(self, status: int):
        self._status = status

    def get_plugin(self, _, __):
        return Response(status=self._status)


@pytest.fixture
def plugin_loader():
    return MagicMock()


def test_get_plugin_not_found(plugin_loader, tmp_path):
    plugin_registry = PluginRegistry(StubIslandAPIClient(status=404), plugin_loader, tmp_path)

    with pytest.raises(UnknownPluginError):
        plugin_registry.get_plugin("Ghost", AgentPluginType.PAYLOAD)


# modify when plugin architecture is fully implemented
def test_get_plugin_not_implemented(plugin_loader, tmp_path):
    plugin_registry = PluginRegistry(StubIslandAPIClient(status=200), plugin_loader, tmp_path)

    with pytest.raises(NotImplementedError):
        plugin_registry.get_plugin("Ghost", AgentPluginType.PAYLOAD)


def test_get_plugin_unexpected_response(plugin_loader, tmp_path):
    plugin_registry = PluginRegistry(StubIslandAPIClient(status=100), plugin_loader, tmp_path)

    with pytest.raises(Exception):
        plugin_registry.get_plugin("Ghost", AgentPluginType.PAYLOAD)
