import io
import tarfile
from tarfile import TarFile
from unittest.mock import MagicMock

import pytest

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType
from monkey_island.cc.repositories.plugin_archive_parser import (
    get_plugin_manifest,
    get_plugin_schema,
    get_plugin_source,
    parse_plugin,
)


@pytest.fixture
def plugin_tarfile(plugin_file) -> TarFile:
    return tarfile.open(plugin_file)


@pytest.fixture
def bad_plugin_tarfile(bad_plugin_file) -> TarFile:
    return tarfile.open(bad_plugin_file)


@pytest.fixture
def symlink_tarfile(symlink_plugin_file) -> TarFile:
    return tarfile.open(symlink_plugin_file)


@pytest.fixture
def dir_tarfile(dir_plugin_file) -> TarFile:
    return tarfile.open(dir_plugin_file)


EXPECTED_MANIFEST = AgentPluginManifest(
    name="test",
    plugin_type=AgentPluginType.EXPLOITER,
    supported_operating_systems=(OperatingSystem.WINDOWS, OperatingSystem.LINUX),
    title="dummy-exploiter",
    description="A dummy exploiter",
    safe=True,
)


def test_parse_plugin__single_vendor(plugin_file, plugin_tarfile):
    manifest = get_plugin_manifest(plugin_tarfile)
    schema = get_plugin_schema(plugin_tarfile)
    data = get_plugin_source(plugin_tarfile)

    expected_agent_plugin_object = AgentPlugin(
        plugin_manifest=manifest,
        config_schema=schema,
        source_archive=data,
        host_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
    )
    expected_return = {
        OperatingSystem.WINDOWS: expected_agent_plugin_object,
        OperatingSystem.LINUX: expected_agent_plugin_object,
    }

    with open(plugin_file, "rb") as f:
        ### This will pass once we pass it a plugin with `vendor/``.
        ### We're using `plugin_file` right now which doesn't have one, so it errors.
        assert parse_plugin(io.BytesIO(f.read()), MagicMock()) == expected_return


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


@pytest.mark.parametrize("tarfile_fixture_name", ["symlink_tarfile", "dir_tarfile"])
def test_get_plugin_manifest__ValueError_if_bad(tarfile_fixture_name, request):
    tarfile = request.getfixturevalue(tarfile_fixture_name)
    with pytest.raises(ValueError):
        get_plugin_manifest(tarfile)


@pytest.mark.parametrize("tarfile_fixture_name", ["symlink_tarfile", "dir_tarfile"])
def test_get_plugin_schema__ValueError_if_bad(tarfile_fixture_name, request):
    tarfile = request.getfixturevalue(tarfile_fixture_name)
    with pytest.raises(ValueError):
        get_plugin_schema(tarfile)


@pytest.mark.parametrize("tarfile_fixture_name", ["symlink_tarfile", "dir_tarfile"])
def test_get_plugin_source__ValueError_if_bad(tarfile_fixture_name, request):
    tarfile = request.getfixturevalue(tarfile_fixture_name)
    with pytest.raises(ValueError):
        get_plugin_source(tarfile)
