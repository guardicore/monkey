import io
import tarfile
from pathlib import Path
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
def single_vendor_plugin_tarfile(single_vendor_plugin_file) -> TarFile:
    return tarfile.open(single_vendor_plugin_file)


@pytest.fixture
def two_vendor_plugin_tarfile(two_vendor_plugin_file) -> TarFile:
    return tarfile.open(two_vendor_plugin_file)


@pytest.fixture
def bad_plugin_tarfile(bad_plugin_file) -> TarFile:
    return tarfile.open(bad_plugin_file)


@pytest.fixture
def symlink_tarfile(symlink_plugin_file) -> TarFile:
    return tarfile.open(symlink_plugin_file)


@pytest.fixture
def dir_tarfile(dir_plugin_file) -> TarFile:
    return tarfile.open(dir_plugin_file)


@pytest.fixture
def tmp_data_dir(tmp_path) -> Path:
    return tmp_path / "data_dir"


EXPECTED_MANIFEST = AgentPluginManifest(
    name="test",
    plugin_type=AgentPluginType.EXPLOITER,
    supported_operating_systems=(OperatingSystem.WINDOWS, OperatingSystem.LINUX),
    title="dummy-exploiter",
    description="A dummy exploiter",
    safe=True,
)


def test_parse_plugin__single_vendor(single_vendor_plugin_file, single_vendor_plugin_tarfile):
    manifest = get_plugin_manifest(single_vendor_plugin_tarfile)
    schema = get_plugin_schema(single_vendor_plugin_tarfile)
    data = get_plugin_source(single_vendor_plugin_tarfile)

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

    with open(single_vendor_plugin_file, "rb") as f:
        assert parse_plugin(io.BytesIO(f.read()), MagicMock()) == expected_return


def test_parse_plugin__two_vendors(two_vendor_plugin_file, two_vendor_plugin_tarfile, tmp_data_dir):
    manifest = get_plugin_manifest(two_vendor_plugin_tarfile)
    schema = get_plugin_schema(two_vendor_plugin_tarfile)
    data = b""
    # data = get_plugin_source(two_vendor_plugin_tarfile)

    expected_linux_agent_plugin_object = AgentPlugin(
        plugin_manifest=manifest,
        config_schema=schema,
        source_archive=data,
        host_operating_systems=(OperatingSystem.LINUX,),
    )
    expected_windows_agent_plugin_object = AgentPlugin(
        plugin_manifest=manifest,
        config_schema=schema,
        source_archive=data,
        host_operating_systems=(OperatingSystem.WINDOWS,),
    )
    expected_return = {
        OperatingSystem.WINDOWS: expected_windows_agent_plugin_object,
        OperatingSystem.LINUX: expected_linux_agent_plugin_object,
    }

    with open(two_vendor_plugin_file, "rb") as f:
        assert parse_plugin(io.BytesIO(f.read()), tmp_data_dir) == expected_return

    assert False


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
