from pathlib import Path

import pytest
from tests.utils import assert_directories_equal

from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType
from infection_monkey.puppet import PluginSourceExtractor


def build_agent_plugin(source_tar_path: Path, name="test_plugin") -> AgentPlugin:
    manifest = AgentPluginManifest(name=name, plugin_type=AgentPluginType.EXPLOITER)
    return AgentPlugin(
        plugin_manifest=manifest,
        config_schema={},
        source_archive=read_file_to_bytes(source_tar_path),
    )


def read_file_to_bytes(file_path: Path) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()


@pytest.fixture
def agent_source_archive_path(data_for_tests_dir: Path) -> Path:
    return data_for_tests_dir / "agent_source_archive"


@pytest.fixture
def extractor(tmp_path: Path) -> PluginSourceExtractor:
    return PluginSourceExtractor(tmp_path)


def test_plugin_directory_property(tmp_path: Path, extractor: PluginSourceExtractor):
    assert extractor.plugin_directory == tmp_path


def test_extract_plugin_source(
    tmp_path: Path, agent_source_archive_path: Path, extractor: PluginSourceExtractor
):
    agent_plugin = build_agent_plugin(agent_source_archive_path / "plugin.tar")

    extractor.extract_plugin_source(agent_plugin)

    assert_directories_equal(tmp_path / "test_plugin", agent_source_archive_path / "src")
    print(tmp_path / "test_plugin")
    print(agent_source_archive_path / "src")


def test_zipslip_tar_raises_exception(plugin_data_dir, extractor: PluginSourceExtractor):
    agent_plugin = build_agent_plugin(plugin_data_dir / "zip_slip.tar")

    with pytest.raises(ValueError):
        extractor.extract_plugin_source(agent_plugin)


def test_symlink_tar_raises_exception(plugin_data_dir, extractor: PluginSourceExtractor):
    agent_plugin = build_agent_plugin(plugin_data_dir / "symlink_file.tar")

    with pytest.raises(ValueError):
        extractor.extract_plugin_source(agent_plugin)


def test_device_tar_raises_exception(plugin_data_dir, extractor: PluginSourceExtractor):
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
    agent_source_archive_path, extractor: PluginSourceExtractor, malicious_plugin_name: str
):
    agent_plugin = build_agent_plugin(
        agent_source_archive_path / "plugin.tar", malicious_plugin_name
    )

    with pytest.raises(ValueError):
        extractor.extract_plugin_source(agent_plugin)
