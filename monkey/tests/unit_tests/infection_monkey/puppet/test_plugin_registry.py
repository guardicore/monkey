from unittest.mock import MagicMock

import pytest
from serpentarium import MultiprocessingPlugin, PluginLoader

from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType
from infection_monkey.i_puppet import UnknownPluginError
from infection_monkey.island_api_client import (
    IIslandAPIClient,
    IslandAPIError,
    IslandAPIRequestError,
)
from infection_monkey.puppet import PluginRegistry, PluginSourceExtractor


@pytest.fixture
def dummy_plugin_source_extractor() -> PluginSourceExtractor:
    return MagicMock(spec=PluginSourceExtractor)


@pytest.fixture
def dummy_plugin_loader() -> PluginLoader:
    return MagicMock(spec=PluginLoader)


def test_get_plugin__unexpected_response(
    dummy_plugin_source_extractor: PluginSourceExtractor, dummy_plugin_loader: PluginLoader
):
    mock_island_api_client = MagicMock()
    mock_island_api_client.get_agent_plugin = MagicMock(side_effect=IslandAPIError)
    plugin_registry = PluginRegistry(
        mock_island_api_client, dummy_plugin_source_extractor, dummy_plugin_loader
    )

    with pytest.raises(IslandAPIError):
        plugin_registry.get_plugin("Ghost", AgentPluginType.PAYLOAD)


def test_get_plugin__unknown_plugin(
    dummy_plugin_source_extractor: PluginSourceExtractor, dummy_plugin_loader: PluginLoader
):
    mock_island_api_client = MagicMock()
    mock_island_api_client.get_agent_plugin = MagicMock(side_effect=IslandAPIRequestError)
    plugin_registry = PluginRegistry(
        mock_island_api_client, dummy_plugin_source_extractor, dummy_plugin_loader
    )

    with pytest.raises(UnknownPluginError):
        plugin_registry.get_plugin("Ghost", AgentPluginType.PAYLOAD)


PLUGIN_NAME = "test_plugin"


@pytest.fixture
def agent_plugin() -> AgentPlugin:
    manifest = AgentPluginManifest(name=PLUGIN_NAME, plugin_type=AgentPluginType.EXPLOITER)
    return AgentPlugin(plugin_manifest=manifest, config_schema={}, source_archive=b"1234")


@pytest.fixture
def mock_island_api_client(agent_plugin) -> IIslandAPIClient:
    mock_island_api_client = MagicMock(spec=IIslandAPIClient)
    mock_island_api_client.get_agent_plugin = MagicMock(return_value=agent_plugin)

    return mock_island_api_client


@pytest.fixture
def mock_plugin_source_extractor() -> PluginSourceExtractor:
    return MagicMock(spec=PluginSourceExtractor)


@pytest.fixture
def mock_plugin_loader() -> PluginLoader:
    mock_plugin = MagicMock(spec=MultiprocessingPlugin)
    mock_plugin_loader = MagicMock(spec=PluginLoader)
    mock_plugin_loader.load_multiprocessing_plugin = MagicMock(return_value=mock_plugin)

    return mock_plugin_loader


def test_load_plugin_from_island__only_downloaded_once(
    agent_plugin: AgentPlugin,
    mock_island_api_client: IIslandAPIClient,
    mock_plugin_source_extractor: PluginSourceExtractor,
    mock_plugin_loader: PluginLoader,
):
    plugin_registry = PluginRegistry(
        mock_island_api_client, mock_plugin_source_extractor, mock_plugin_loader
    )

    plugin_registry.get_plugin(PLUGIN_NAME, AgentPluginType.EXPLOITER)
    plugin_registry.get_plugin(PLUGIN_NAME, AgentPluginType.EXPLOITER)

    mock_island_api_client.get_agent_plugin.assert_called_once()
    mock_plugin_source_extractor.extract_plugin_source.assert_called_once()
    mock_plugin_loader.load_multiprocessing_plugin.assert_called_once()
