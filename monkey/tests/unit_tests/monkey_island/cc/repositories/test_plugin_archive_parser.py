import io
import json
import tarfile
from pathlib import Path
from tarfile import TarFile, TarInfo
from typing import Any, BinaryIO, Callable, Dict, Tuple

import pytest
import yaml

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType
from monkey_island.cc.repositories.plugin_archive_parser import (
    get_plugin_manifest,
    get_plugin_schema,
    get_plugin_source,
    parse_plugin,
)


@pytest.fixture
def simple_agent_plugin(build_agent_plugin) -> AgentPlugin:
    fileobj = io.BytesIO()
    with TarFile(fileobj=fileobj, mode="w") as tar:
        plugin_py_tarinfo = TarInfo("plugin.py")
        plugin_py_bytes = b'print("Hello world!")'
        plugin_py_tarinfo.size = len(plugin_py_bytes)
        tar.addfile(plugin_py_tarinfo, io.BytesIO(plugin_py_bytes))
    fileobj.seek(0)

    return build_agent_plugin(source_archive=fileobj.getvalue())


BuildAgentPluginCallable = Callable[[bytes, Tuple[OperatingSystem, ...]], AgentPlugin]


@pytest.fixture
def build_agent_plugin_tar_with_source_tar(build_agent_plugin: BuildAgentPluginCallable):
    def inner(input_tar_path: Path) -> BinaryIO:
        with open(input_tar_path, "rb") as f:
            source_archive = f.read()
            agent_plugin = build_agent_plugin(source_archive, tuple())
            return build_agent_plugin_tar(agent_plugin)

    return inner


@pytest.fixture
def build_agent_plugin(agent_plugin_manifest: AgentPluginManifest, config_schema: Dict[str, Any]):
    def inner(
        source_archive: bytes = b"",
        host_operating_systems: Tuple[OperatingSystem, ...] = (
            OperatingSystem.LINUX,
            OperatingSystem.WINDOWS,
        ),
    ) -> AgentPlugin:
        return AgentPlugin(
            plugin_manifest=agent_plugin_manifest,
            config_schema=config_schema,
            source_archive=source_archive,
            host_operating_systems=host_operating_systems,
        )

    return inner


@pytest.fixture
def agent_plugin_manifest() -> AgentPluginManifest:
    return AgentPluginManifest(
        name="TestPlugin",
        plugin_type=AgentPluginType.EXPLOITER,
        supported_operating_systems=[OperatingSystem.LINUX, OperatingSystem.WINDOWS],
    )


@pytest.fixture
def config_schema() -> Dict[str, Any]:
    return {"type": "object", "properties": {"name": {"type": "string"}}}


def build_agent_plugin_tar(agent_plugin: AgentPlugin) -> BinaryIO:
    fileobj = io.BytesIO()
    with TarFile(fileobj=fileobj, mode="w") as tar:
        manifest_tarinfo = TarInfo("plugin.yaml")
        manifest_bytes = yaml.safe_dump(agent_plugin.plugin_manifest.dict(simplify=True)).encode()
        manifest_tarinfo.size = len(manifest_bytes)
        tar.addfile(manifest_tarinfo, io.BytesIO(manifest_bytes))

        config_schema_tarinfo = TarInfo("config-schema.json")
        config_schema_bytes = json.dumps(agent_plugin.config_schema).encode()
        config_schema_tarinfo.size = len(config_schema_bytes)
        tar.addfile(config_schema_tarinfo, io.BytesIO(config_schema_bytes))

        plugin_source_archive_tarinfo = TarInfo("plugin.tar")
        plugin_source_archive_tarinfo.size = len(agent_plugin.source_archive)
        tar.addfile(plugin_source_archive_tarinfo, io.BytesIO(agent_plugin.source_archive))

    fileobj.seek(0)
    return fileobj


def test_parse_plugin_manifest(
    simple_agent_plugin: AgentPlugin, agent_plugin_manifest: AgentPluginManifest
):
    agent_plugin_tar = build_agent_plugin_tar(simple_agent_plugin)
    parsed_plugin = parse_plugin(agent_plugin_tar)

    for plugin in parsed_plugin.values():
        assert plugin.plugin_manifest == agent_plugin_manifest


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
    actual = TarFile(fileobj=io.BytesIO(actual_source_archive))

    with TarFile(fileobj=io.BytesIO(actual_source_archive)) as actual:
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


# --------------------------------------------------------------------------------------------------


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
