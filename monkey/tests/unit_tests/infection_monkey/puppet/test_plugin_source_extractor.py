from pathlib import Path

import pytest
from tests.utils import assert_directories_equal

from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType
from infection_monkey.puppet import PluginSourceExtractor


def build_agent_plugin(source_tar_path: Path) -> AgentPlugin:
    manifest = AgentPluginManifest(name="test_plugin", plugin_type=AgentPluginType.EXPLOITER)
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
