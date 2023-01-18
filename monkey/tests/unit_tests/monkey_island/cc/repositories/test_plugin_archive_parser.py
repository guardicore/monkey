import io
import os
import tarfile
from tarfile import TarFile
from unittest.mock import MagicMock

import pytest

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType
from monkey_island.cc.repositories.plugin_archive_parser import (
    get_os_specific_plugin_source_archives,
    get_plugin_manifest,
    get_plugin_schema,
    get_plugin_source,
    get_plugin_source_vendors,
    parse_plugin,
)


@pytest.fixture
def plugin_tarfile(plugin_file) -> TarFile:
    return tarfile.open(plugin_file)


@pytest.fixture
def plugin_with_one_vendor_tarfile(plugin_with_one_vendor_file) -> TarFile:
    return tarfile.open(plugin_with_one_vendor_file)


@pytest.fixture
def plugin_with_two_vendors_tarfile(plugin_with_two_vendors_file) -> TarFile:
    return tarfile.open(plugin_with_two_vendors_file)


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
def plugin_with_three_vendors_tarfile(plugin_with_three_vendors_file) -> TarFile:
    return tarfile.open(plugin_with_three_vendors_file)


@pytest.fixture
def plugin_with_two_vendor_dirs_one_vendor_file_tarfile(
    plugin_with_two_vendor_dirs_one_vendor_file_file,
) -> TarFile:
    return tarfile.open(plugin_with_two_vendor_dirs_one_vendor_file_file)


@pytest.fixture
def only_windows_vendor_plugin_tarfile(only_windows_vendor_plugin_file) -> TarFile:
    return tarfile.open(only_windows_vendor_plugin_file)


def _get_plugin_source_tar(tarfile_):
    return TarFile(fileobj=io.BytesIO(get_plugin_source(tarfile_)))


def test_get_os_specific_plugin_source_archives(plugin_with_two_vendors_tarfile, tmp_path):
    plugin_source_tar = _get_plugin_source_tar(plugin_with_two_vendors_tarfile)
    plugin_vendors = get_plugin_source_vendors(plugin_source_tar)
    os_specific_data = get_os_specific_plugin_source_archives(
        tmp_path, plugin_source_tar, plugin_vendors
    )

    assert os_specific_data[OperatingSystem.WINDOWS] != os_specific_data[OperatingSystem.LINUX]

    assert not os.path.exists(tmp_path / "linux")
    assert not os.path.exists(tmp_path / "windows")


def test_get_os_specific_plugin_source_archives__only_windows(
    only_windows_vendor_plugin_tarfile, tmp_path
):
    plugin_source_tar = _get_plugin_source_tar(only_windows_vendor_plugin_tarfile)
    plugin_vendors = get_plugin_source_vendors(plugin_source_tar)
    os_specific_data = get_os_specific_plugin_source_archives(
        tmp_path, plugin_source_tar, plugin_vendors
    )

    assert len(os_specific_data.keys()) == 1
    assert list(os_specific_data.keys()) == [OperatingSystem.WINDOWS]

    assert not os.path.exists(tmp_path / "linux")
    assert not os.path.exists(tmp_path / "windows")


def test_get_os_specific_plugin_source_archives__unrecognised_os(
    plugin_with_three_vendors_tarfile, tmp_path
):
    plugin_source_tar = _get_plugin_source_tar(plugin_with_three_vendors_tarfile)
    plugin_vendors = get_plugin_source_vendors(plugin_source_tar)
    os_specific_data = get_os_specific_plugin_source_archives(
        tmp_path, plugin_source_tar, plugin_vendors
    )

    assert len(os_specific_data.keys()) == 0
    assert list(os_specific_data.keys()) == []

    assert not os.path.exists(tmp_path / "linux")
    assert not os.path.exists(tmp_path / "windows")


def test_get_plugin_vendors__3_vendor_dirs(plugin_with_three_vendors_tarfile):
    plugin_source_tarfile = _get_plugin_source_tar(plugin_with_three_vendors_tarfile)
    vendors = get_plugin_source_vendors(plugin_source_tarfile)

    assert len(vendors) == 3


def test_get_plugin_vendors__2_vendor_dirs_1_Vendor_file(
    plugin_with_two_vendor_dirs_one_vendor_file_tarfile,
):
    plugin_source_tarfile = _get_plugin_source_tar(
        plugin_with_two_vendor_dirs_one_vendor_file_tarfile
    )
    vendors = get_plugin_source_vendors(plugin_source_tarfile)

    assert len(vendors) == 2


def test_parse_plugin__single_vendor(plugin_with_one_vendor_file, plugin_with_one_vendor_tarfile):
    manifest = get_plugin_manifest(plugin_with_one_vendor_tarfile)
    schema = get_plugin_schema(plugin_with_one_vendor_tarfile)
    data = get_plugin_source(plugin_with_one_vendor_tarfile)

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

    with open(plugin_with_one_vendor_file, "rb") as f:
        assert parse_plugin(io.BytesIO(f.read()), MagicMock()) == expected_return


def test_parse_plugin__two_vendors(
    plugin_with_two_vendors_file, plugin_with_two_vendors_tarfile, tmp_path
):
    manifest = get_plugin_manifest(plugin_with_two_vendors_tarfile)
    schema = get_plugin_schema(plugin_with_two_vendors_tarfile)

    parsed_plugins_dir = tmp_path / "parsed_plugins"
    os.mkdir(parsed_plugins_dir)

    plugin_source_tar = TarFile(
        fileobj=io.BytesIO(get_plugin_source(plugin_with_two_vendors_tarfile))
    )
    plugin_vendors = get_plugin_source_vendors(plugin_source_tar)
    os_specific_data = get_os_specific_plugin_source_archives(
        parsed_plugins_dir, plugin_source_tar, plugin_vendors
    )

    expected_linux_agent_plugin_object = AgentPlugin(
        plugin_manifest=manifest,
        config_schema=schema,
        source_archive=os_specific_data[OperatingSystem.LINUX],
        host_operating_systems=(OperatingSystem.LINUX,),
    )
    expected_windows_agent_plugin_object = AgentPlugin(
        plugin_manifest=manifest,
        config_schema=schema,
        source_archive=os_specific_data[OperatingSystem.WINDOWS],
        host_operating_systems=(OperatingSystem.WINDOWS,),
    )
    expected_return = {
        OperatingSystem.WINDOWS: expected_windows_agent_plugin_object,
        OperatingSystem.LINUX: expected_linux_agent_plugin_object,
    }

    with open(plugin_with_two_vendors_file, "rb") as f:
        actual_return = parse_plugin(io.BytesIO(f.read()), tmp_path)

    assert actual_return == expected_return

    assert list(parsed_plugins_dir.iterdir()) == []


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
