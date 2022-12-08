import tarfile
from pathlib import Path
from tarfile import TarFile

import pytest

from common import OperatingSystem
from common.agent_plugins import AgentPluginManifest, AgentPluginType
from monkey_island.cc.repositories.plugin_archive_parser import (
    get_plugin_manifest,
    get_plugin_schema,
    get_plugin_source,
)


@pytest.fixture
def plugin_tarfile(plugin_file) -> TarFile:
    return tarfile.open(plugin_file)


@pytest.fixture
def bad_plugin_tarfile(bad_plugin_file) -> TarFile:
    return tarfile.open(bad_plugin_file)


EXPECTED_MANIFEST = AgentPluginManifest(
    name="test",
    plugin_type=AgentPluginType.EXPLOITER,
    supported_operating_systems=(OperatingSystem.WINDOWS, OperatingSystem.LINUX),
    title="dummy-exploiter",
    description="A dummy exploiter",
    safe=True,
)


def test_get_plugin_manifest(plugin_tarfile):
    expected = EXPECTED_MANIFEST
    actual = get_plugin_manifest(plugin_tarfile)

    assert actual == expected


def test_get_plugin_schema(plugin_tarfile):
    expected = {"type": "object", "properties": {"name": {"type": "string"}}}

    schema = get_plugin_schema(plugin_tarfile)

    assert schema == expected


def test_get_plugin_source(plugin_tarfile):
    data = get_plugin_source(plugin_tarfile)

    assert len(data) == 10240


def test_get_plugin_manifest__KeyError_if_missing(bad_plugin_tarfile):
    with pytest.raises(KeyError):
        get_plugin_manifest(bad_plugin_tarfile)


def test_get_plugin_schema__KeyError_if_missing(bad_plugin_tarfile):
    with pytest.raises(KeyError):
        get_plugin_schema(bad_plugin_tarfile)


def test_get_plugin_source_KeyError_if_missing(bad_plugin_tarfile):
    with pytest.raises(KeyError):
        get_plugin_source(bad_plugin_tarfile)


def test_get_plugin_manifest__ValueError_if_bad(monkeypatch, plugin_tarfile):
    monkeypatch.setattr(tarfile.TarFile, "extractfile", lambda a, b: None)
    with pytest.raises(ValueError):
        get_plugin_manifest(plugin_tarfile)


def test_get_plugin_schema__ValueError_if_bad(monkeypatch, plugin_tarfile):
    monkeypatch.setattr(tarfile.TarFile, "extractfile", lambda a, b: None)
    with pytest.raises(ValueError):
        get_plugin_schema(plugin_tarfile)


def test_get_plugin_source__ValueError_if_bad(monkeypatch, plugin_tarfile):
    monkeypatch.setattr(tarfile.TarFile, "extractfile", lambda a, b: None)
    with pytest.raises(ValueError):
        get_plugin_source(plugin_tarfile)
