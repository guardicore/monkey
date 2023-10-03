import gzip
import io
import tarfile
from pathlib import Path
from tarfile import TarFile
from typing import Any, BinaryIO, Callable, Dict

import pytest
from monkeytypes import AgentPluginType
from tests.unit_tests.monkey_island.cc.services.agent_plugin_service.conftest import (
    build_agent_plugin_tar,
)

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest
from monkey_island.cc.services.agent_plugin_service.plugin_archive_parser import (
    VendorDirName,
    get_plugin_manifest,
    get_plugin_schema,
    get_plugin_source,
    parse_plugin,
)


def test_parse_plugin_manifest_yaml_extension(
    simple_agent_plugin: AgentPlugin, agent_plugin_manifest: AgentPluginManifest
):
    agent_plugin_tar = build_agent_plugin_tar(simple_agent_plugin)
    parsed_plugin = parse_plugin(agent_plugin_tar)

    for plugin in parsed_plugin.values():
        assert plugin.plugin_manifest == agent_plugin_manifest


def test_parse_plugin_manifest_yml_extension(
    simple_agent_plugin: AgentPlugin, agent_plugin_manifest: AgentPluginManifest
):
    agent_plugin_tar = build_agent_plugin_tar(
        simple_agent_plugin, manifest_file_name="manifest.yml"
    )
    parsed_plugin = parse_plugin(agent_plugin_tar)

    for plugin in parsed_plugin.values():
        assert plugin.plugin_manifest == agent_plugin_manifest


def test_parse_plugin_manifest_unrecognised_extension(
    simple_agent_plugin: AgentPlugin, agent_plugin_manifest: AgentPluginManifest
):
    agent_plugin_tar = build_agent_plugin_tar(
        simple_agent_plugin, manifest_file_name="manifest.idk"
    )

    with pytest.raises(ValueError):
        parse_plugin(agent_plugin_tar)


def test_parse_plugin_config_schema(
    simple_agent_plugin: AgentPlugin, config_schema: Dict[str, Any]
):
    agent_plugin_tar = build_agent_plugin_tar(simple_agent_plugin)
    parsed_plugin = parse_plugin(agent_plugin_tar)

    for plugin in parsed_plugin.values():
        assert plugin.config_schema == config_schema


def assert_parsed_plugin_archive_equals_expected(
    actual_source_archive: bytes, expected_tar_path: Path
):
    decompressed_actual_source_archive = gzip.decompress(actual_source_archive)
    with TarFile(fileobj=io.BytesIO(decompressed_actual_source_archive)) as actual:
        with open(expected_tar_path, "rb") as f:
            with TarFile(fileobj=f) as expected:
                assert actual.getnames() == expected.getnames()
                assert len(actual.getmembers()) == len(expected.getmembers())

                for member in actual.getmembers():
                    a = actual.extractfile(member)
                    e = expected.extractfile(member)
                    if a is None or e is None:
                        assert a == e
                    else:
                        assert a.read() == e.read()


def test_parse_windows_vendor_only(
    plugin_data_dir: Path, build_agent_plugin_tar_with_source_tar: Callable[[Path], BinaryIO]
):
    agent_plugin_tar = build_agent_plugin_tar_with_source_tar(
        plugin_data_dir / "only-windows-vendor-plugin-source-input.tar"
    )

    parsed_plugin = parse_plugin(agent_plugin_tar)

    assert OperatingSystem.LINUX not in parsed_plugin
    assert_parsed_plugin_archive_equals_expected(
        parsed_plugin[OperatingSystem.WINDOWS].source_archive,
        plugin_data_dir / "only-windows-vendor-plugin-source-expected-output.tar",
    )


def test_parse_linux_vendor_only(
    plugin_data_dir: Path, build_agent_plugin_tar_with_source_tar: Callable[[Path], BinaryIO]
):
    agent_plugin_tar = build_agent_plugin_tar_with_source_tar(
        plugin_data_dir / "only-linux-vendor-plugin-source-input.tar"
    )

    parsed_plugin = parse_plugin(agent_plugin_tar)

    assert OperatingSystem.WINDOWS not in parsed_plugin
    assert_parsed_plugin_archive_equals_expected(
        parsed_plugin[OperatingSystem.LINUX].source_archive,
        plugin_data_dir / "only-linux-vendor-plugin-source-expected-output.tar",
    )


def test_parse_multi_vendor(
    plugin_data_dir: Path, build_agent_plugin_tar_with_source_tar: Callable[[Path], BinaryIO]
):
    agent_plugin_tar = build_agent_plugin_tar_with_source_tar(
        plugin_data_dir / "multi-vendor-plugin-source-input.tar"
    )

    parsed_plugin = parse_plugin(agent_plugin_tar)

    assert_parsed_plugin_archive_equals_expected(
        parsed_plugin[OperatingSystem.LINUX].source_archive,
        plugin_data_dir / "multi-vendor-plugin-source-expected-linux-output.tar",
    )
    assert_parsed_plugin_archive_equals_expected(
        parsed_plugin[OperatingSystem.WINDOWS].source_archive,
        plugin_data_dir / "multi-vendor-plugin-source-expected-windows-output.tar",
    )


def test_parse_cross_platform(
    plugin_data_dir: Path, build_agent_plugin_tar_with_source_tar: Callable[[Path], BinaryIO]
):
    agent_plugin_tar = build_agent_plugin_tar_with_source_tar(
        plugin_data_dir / "cross-platform-plugin-source.tar"
    )

    parsed_plugin = parse_plugin(agent_plugin_tar)

    assert_parsed_plugin_archive_equals_expected(
        parsed_plugin[OperatingSystem.LINUX].source_archive,
        plugin_data_dir / "cross-platform-plugin-source.tar",
    )
    assert_parsed_plugin_archive_equals_expected(
        parsed_plugin[OperatingSystem.WINDOWS].source_archive,
        plugin_data_dir / "cross-platform-plugin-source.tar",
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
    supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
    target_operating_systems=(OperatingSystem.WINDOWS, OperatingSystem.LINUX),
    title="dummy-exploiter",
    version="1.0.0",
    description="A dummy exploiter",
    safe=True,
)


def test_get_plugin_manifest(plugin_tarfile):
    expected = EXPECTED_MANIFEST
    actual = get_plugin_manifest(plugin_tarfile)

    assert actual == expected


def test_missing_manifest(missing_manifest_plugin_file):
    with open(missing_manifest_plugin_file, "rb") as f:
        with pytest.raises(ValueError):
            parse_plugin(f)


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


@pytest.mark.parametrize(
    "input_vendor_dir_name, expected_os",
    [
        (VendorDirName.LINUX_VENDOR, OperatingSystem.LINUX),
        (VendorDirName.WINDOWS_VENDOR, OperatingSystem.WINDOWS),
    ],
)
def test_to_operating_system(input_vendor_dir_name: VendorDirName, expected_os: OperatingSystem):
    assert VendorDirName.to_operating_system(input_vendor_dir_name) == expected_os


def test_to_operating_system__raises_ValueError():
    with pytest.raises(ValueError):
        VendorDirName.to_operating_system(VendorDirName.ANY_VENDOR)
