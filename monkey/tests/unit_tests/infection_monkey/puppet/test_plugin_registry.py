from unittest.mock import MagicMock

import pytest
from serpentarium import MultiprocessingPlugin, PluginLoader

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest, AgentPluginType
from common.event_queue import IAgentEventPublisher
from infection_monkey.exploit import IAgentBinaryRepository
from infection_monkey.i_puppet import UnknownPluginError
from infection_monkey.island_api_client import (
    IIslandAPIClient,
    IslandAPIError,
    IslandAPIRequestError,
)
from infection_monkey.propagation_credentials_repository import IPropagationCredentialsRepository
from infection_monkey.puppet import PluginRegistry, PluginSourceExtractor


@pytest.fixture
def dummy_plugin_source_extractor() -> PluginSourceExtractor:
    return MagicMock(spec=PluginSourceExtractor)


@pytest.fixture
def dummy_plugin_loader() -> PluginLoader:
    return MagicMock(spec=PluginLoader)


@pytest.fixture
def dummy_agent_binary_repository() -> IAgentBinaryRepository:
    return MagicMock(spec=IAgentBinaryRepository)


@pytest.fixture
def dummy_agent_event_publisher() -> IAgentEventPublisher:
    return MagicMock(spec=IAgentEventPublisher)


@pytest.fixture
def dummy_propagation_credentials_repository() -> IPropagationCredentialsRepository:
    return MagicMock(spec=IPropagationCredentialsRepository)


@pytest.mark.parametrize(
    "error_raised_by_island_api_client, error_raised_by_plugin_registry",
    [(IslandAPIRequestError, UnknownPluginError), (IslandAPIError, IslandAPIError)],
)
def test_get_plugin__error_handling(
    dummy_plugin_source_extractor: PluginSourceExtractor,
    dummy_plugin_loader: PluginLoader,
    dummy_agent_binary_repository: IAgentBinaryRepository,
    dummy_agent_event_publisher: IAgentEventPublisher,
    dummy_propagation_credentials_repository: IPropagationCredentialsRepository,
    error_raised_by_island_api_client: Exception,
    error_raised_by_plugin_registry: Exception,
):
    mock_island_api_client = MagicMock()
    mock_island_api_client.get_agent_plugin = MagicMock(
        side_effect=error_raised_by_island_api_client
    )
    plugin_registry = PluginRegistry(
        OperatingSystem.LINUX,
        mock_island_api_client,
        dummy_plugin_source_extractor,
        dummy_plugin_loader,
        dummy_agent_binary_repository,
        dummy_agent_event_publisher,
        dummy_propagation_credentials_repository,
    )

    with pytest.raises(error_raised_by_plugin_registry):
        plugin_registry.get_plugin(AgentPluginType.PAYLOAD, "Ghost")


PLUGIN_NAME = "test_plugin"


@pytest.fixture
def agent_plugin() -> AgentPlugin:
    manifest = AgentPluginManifest(name=PLUGIN_NAME, plugin_type=AgentPluginType.EXPLOITER)
    return AgentPlugin(
        plugin_manifest=manifest,
        config_schema={},
        source_archive=b"1234",
        host_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
    )


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


@pytest.fixture
def plugin_registry(
    mock_island_api_client: IIslandAPIClient,
    mock_plugin_source_extractor: PluginSourceExtractor,
    mock_plugin_loader: PluginLoader,
    dummy_agent_binary_repository: IAgentBinaryRepository,
    dummy_agent_event_publisher: IAgentEventPublisher,
    dummy_propagation_credentials_repository: IPropagationCredentialsRepository,
) -> PluginRegistry:
    return PluginRegistry(
        OperatingSystem.LINUX,
        mock_island_api_client,
        mock_plugin_source_extractor,
        mock_plugin_loader,
        dummy_agent_binary_repository,
        dummy_agent_event_publisher,
        dummy_propagation_credentials_repository,
    )


def test_load_plugin_from_island__only_downloaded_once(
    agent_plugin: AgentPlugin,
    mock_island_api_client: IIslandAPIClient,
    mock_plugin_source_extractor: PluginSourceExtractor,
    mock_plugin_loader: PluginLoader,
    plugin_registry: PluginRegistry,
):
    plugin_registry.get_plugin(AgentPluginType.EXPLOITER, PLUGIN_NAME)
    plugin_registry.get_plugin(AgentPluginType.EXPLOITER, PLUGIN_NAME)

    mock_island_api_client.get_agent_plugin.assert_called_once()
    mock_plugin_source_extractor.extract_plugin_source.assert_called_once()
    mock_plugin_loader.load_multiprocessing_plugin.assert_called_once()


def test_load_plugin_from_island__return_copy(
    agent_plugin: AgentPlugin,
    mock_island_api_client: IIslandAPIClient,
    mock_plugin_source_extractor: PluginSourceExtractor,
    mock_plugin_loader: PluginLoader,
    plugin_registry: PluginRegistry,
):
    plugin1 = plugin_registry.get_plugin(AgentPluginType.EXPLOITER, PLUGIN_NAME)
    plugin2 = plugin_registry.get_plugin(AgentPluginType.EXPLOITER, PLUGIN_NAME)

    assert plugin1.__class__ == plugin2.__class__
    assert plugin1.name == plugin2.name
    assert id(plugin1) != id(plugin2)
