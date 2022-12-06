import tarfile
from pathlib import Path
from tarfile import TarFile

import pytest

from common import OperatingSystem
from common.agent_plugins import AgentPluginManifest, AgentPluginType
from monkey_island.cc.repositories.plugin_utils import TarPluginLoader


@pytest.fixture
def manifest_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "manifest.yaml"


@pytest.fixture
def plugin_file(plugin_data_dir) -> Path:
    return plugin_data_dir / "test-exploiter.tar"


@pytest.fixture
def plugin_tarfile(plugin_file) -> TarFile:
    return tarfile.open(plugin_file)


def test_get_plugin_manifest(plugin_tarfile):
    expected = AgentPluginManifest(
        name="test",
        plugin_type=AgentPluginType.EXPLOITER,
        supported_operating_systems=(OperatingSystem.WINDOWS, OperatingSystem.LINUX),
        title="dummy-exploiter",
        description="A dummy exploiter",
        safe=True,
    )

    actual = TarPluginLoader.get_plugin_manifest(plugin_tarfile)

    assert actual == expected


def test_get_plugin_schema(plugin_tarfile):
    schema = TarPluginLoader.get_plugin_schema(plugin_tarfile)

    assert isinstance(schema, dict)


def test_get_plugin_source(plugin_tarfile):
    data = TarPluginLoader.get_plugin_source(plugin_tarfile)

    assert len(data) > 0
