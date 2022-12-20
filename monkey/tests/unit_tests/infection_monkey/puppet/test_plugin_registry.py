from unittest.mock import MagicMock

import pytest

from common.agent_plugins import AgentPluginType
from infection_monkey.i_puppet import UnknownPluginError
from infection_monkey.island_api_client import IslandAPIError, IslandAPIRequestError
from infection_monkey.puppet import PluginRegistry


@pytest.fixture
def dummy_plugin_source_extractor():
    return MagicMock()


@pytest.fixture
def dummy_plugin_loader():
    return MagicMock()


def test_get_plugin__unexpected_response(dummy_plugin_source_extractor, dummy_plugin_loader):
    mock_island_api_client = MagicMock()
    mock_island_api_client.get_agent_plugin = MagicMock(side_effect=IslandAPIError)
    plugin_registry = PluginRegistry(
        mock_island_api_client, dummy_plugin_source_extractor, dummy_plugin_loader
    )

    with pytest.raises(IslandAPIError):
        plugin_registry.get_plugin("Ghost", AgentPluginType.PAYLOAD)


def test_get_plugin__unknown_plugin(dummy_plugin_source_extractor, dummy_plugin_loader):
    mock_island_api_client = MagicMock()
    mock_island_api_client.get_agent_plugin = MagicMock(side_effect=IslandAPIRequestError)
    plugin_registry = PluginRegistry(
        mock_island_api_client, dummy_plugin_source_extractor, dummy_plugin_loader
    )

    with pytest.raises(UnknownPluginError):
        plugin_registry.get_plugin("Ghost", AgentPluginType.PAYLOAD)
