import gzip
from pathlib import Path

import pytest
from monkeytypes import AgentPluginManifest, AgentPluginType
from tests.utils import assert_directories_equal

from common import OperatingSystem
from common.agent_plugins import AgentPlugin
from common.utils.environment import is_windows_os
from infection_monkey.puppet import PluginSourceExtractor


def build_agent_plugin(source_tar_path: Path, name="test_plugin") -> AgentPlugin:
    # We're using construct() here because we want to be able to construct plugins with invalid
    # names. Specifically, this is used for in test_plugin_name_directory_traversal()
    manifest = AgentPluginManifest.construct(name=name, plugin_type=AgentPluginType.EXPLOITER)
    return AgentPlugin.construct(
        plugin_manifest=manifest,
        config_schema={},
        source_archive=gzip.compress(read_file_to_bytes(source_tar_path), compresslevel=1),
        supported_operating_systems=(OperatingSystem.WINDOWS,),
    )


def read_file_to_bytes(file_path: Path) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()


@pytest.fixture
def dircmp_path(data_for_tests_dir: Path) -> Path:
    return data_for_tests_dir / "dircmp"


@pytest.fixture
def extractor(tmp_path: Path) -> PluginSourceExtractor:
    return PluginSourceExtractor(tmp_path)


def test_plugin_destination_directory_property(tmp_path: Path, extractor: PluginSourceExtractor):
    assert extractor.plugin_destination_directory == tmp_path


def test_extract_plugin_source(tmp_path: Path, dircmp_path: Path, extractor: PluginSourceExtractor):
    if is_windows_os():
        agent_plugin = build_agent_plugin(dircmp_path / "dir1_win.tar")
    else:
        agent_plugin = build_agent_plugin(dircmp_path / "dir1.tar")

    extractor.extract_plugin_source(agent_plugin)

    assert_directories_equal(tmp_path / "test_plugin", dircmp_path / "dir1")


def test_zipslip_tar_raises_exception(plugin_data_dir: Path, extractor: PluginSourceExtractor):
    agent_plugin = build_agent_plugin(plugin_data_dir / "zip_slip.tar")

    with pytest.raises(ValueError):
        extractor.extract_plugin_source(agent_plugin)


def test_symlink_tar_raises_exception(plugin_data_dir: Path, extractor: PluginSourceExtractor):
    agent_plugin = build_agent_plugin(plugin_data_dir / "symlink_file.tar")

    with pytest.raises(ValueError):
        extractor.extract_plugin_source(agent_plugin)


def test_device_tar_raises_exception(plugin_data_dir: Path, extractor: PluginSourceExtractor):
    agent_plugin = build_agent_plugin(plugin_data_dir / "device.tar")

    with pytest.raises(ValueError):
        extractor.extract_plugin_source(agent_plugin)


@pytest.mark.parametrize(
    "malicious_plugin_name",
    [
        "../test_dir12341234",
        "../../test_dir12341234",
        "../../../../../../../test_dir12341234",
        "/test_dir12341234",
        "test_dir/../../../12341234",
        "test_dir/../../../",
        "../../../",
        "..",
        ".",
    ],
)
def test_plugin_name_directory_traversal(
    dircmp_path: Path, extractor: PluginSourceExtractor, malicious_plugin_name: str
):
    agent_plugin = build_agent_plugin(dircmp_path / "dir1.tar", malicious_plugin_name)

    with pytest.raises(ValueError):
        extractor.extract_plugin_source(agent_plugin)


def test_extract_nongzip_raises_value_error(dircmp_path: Path, extractor: PluginSourceExtractor):
    source_tar_path = dircmp_path / "dir1.tar"
    manifest = AgentPluginManifest.construct(name="test", plugin_type=AgentPluginType.EXPLOITER)
    agent_plugin = AgentPlugin.construct(
        plugin_manifest=manifest,
        config_schema={},
        source_archive=read_file_to_bytes(source_tar_path),  # Not gzipped
        supported_operating_systems=(OperatingSystem.WINDOWS,),
    )
    with pytest.raises(ValueError):
        extractor.extract_plugin_source(agent_plugin)
