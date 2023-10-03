from typing import Dict
from unittest.mock import MagicMock

import pytest
from monkeytypes import AgentPluginType
from serpentarium import MultiprocessingPlugin, PluginLoader, SingleUsePlugin

from common import OperatingSystem
from common.agent_plugins import AgentPlugin, AgentPluginManifest
from common.event_queue import IAgentEventPublisher
from common.types import AgentID
from infection_monkey.exploit import IAgentBinaryRepository, IAgentOTPProvider
from infection_monkey.i_puppet import UnknownPluginError
from infection_monkey.island_api_client import (
    IIslandAPIClient,
    IslandAPIError,
    IslandAPIRequestError,
)
from infection_monkey.network import TCPPortSelector
from infection_monkey.plugin.i_plugin_factory import IPluginFactory
from infection_monkey.propagation_credentials_repository import IPropagationCredentialsRepository
from infection_monkey.puppet import PluginRegistry, PluginSourceExtractor

AGENT_ID = AgentID("707d801b-68cf-44d1-8a4e-7e1a89c412f8")


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


@pytest.fixture
def dummy_tcp_port_selector() -> TCPPortSelector:
    return MagicMock(spec=TCPPortSelector)


@pytest.fixture
def dummy_otp_provider() -> IAgentOTPProvider:
    return MagicMock(spec=IAgentOTPProvider)


@pytest.mark.parametrize(
    "error_raised_by_island_api_client, error_raised_by_plugin_registry",
    [(IslandAPIRequestError, UnknownPluginError), (IslandAPIError, IslandAPIError)],
)
def test_get_plugin__error_handling(
    dummy_plugin_source_extractor: PluginSourceExtractor,
    mock_plugin_factories: Dict[AgentPluginType, IPluginFactory],
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
        mock_plugin_factories,
    )

    with pytest.raises(error_raised_by_plugin_registry):
        plugin_registry.get_plugin(AgentPluginType.PAYLOAD, "Ghost")


PLUGIN_NAME = "test_plugin"


def agent_plugin_of_type(plugin_type: AgentPluginType) -> AgentPlugin:
    manifest = AgentPluginManifest(name=PLUGIN_NAME, version="1.0.0", plugin_type=plugin_type)
    return AgentPlugin(
        plugin_manifest=manifest,
        config_schema={},
        source_archive=b"1234",
        supported_operating_systems=(OperatingSystem.LINUX, OperatingSystem.WINDOWS),
    )


@pytest.fixture
def agent_plugin() -> AgentPlugin:
    return agent_plugin_of_type(AgentPluginType.EXPLOITER)


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
def mock_plugin_factories() -> Dict[AgentPluginType, IPluginFactory]:
    return {
        AgentPluginType.EXPLOITER: MagicMock(spec=IPluginFactory),
        AgentPluginType.CREDENTIALS_COLLECTOR: MagicMock(spec=IPluginFactory),
        AgentPluginType.PAYLOAD: MagicMock(spec=IPluginFactory),
    }


@pytest.fixture
def plugin_registry(
    mock_island_api_client: IIslandAPIClient,
    mock_plugin_source_extractor: PluginSourceExtractor,
    mock_plugin_factories,
) -> PluginRegistry:
    return PluginRegistry(
        OperatingSystem.LINUX,
        mock_island_api_client,
        mock_plugin_source_extractor,
        mock_plugin_factories,
    )


def test_load_plugin_from_island__only_downloaded_once(
    agent_plugin: AgentPlugin,
    mock_island_api_client: IIslandAPIClient,
    mock_plugin_source_extractor: PluginSourceExtractor,
    plugin_registry: PluginRegistry,
):
    plugin_registry.get_plugin(AgentPluginType.EXPLOITER, PLUGIN_NAME)
    plugin_registry.get_plugin(AgentPluginType.EXPLOITER, PLUGIN_NAME)

    mock_island_api_client.get_agent_plugin.assert_called_once()
    mock_plugin_source_extractor.extract_plugin_source.assert_called_once()


def test_load_plugin_from_island__return_copy(
    mock_plugin_factories: Dict[AgentPluginType, IPluginFactory],
    plugin_registry: PluginRegistry,
):
    mock_plugin_factories[AgentPluginType.EXPLOITER].create.return_value = MagicMock(
        spec=SingleUsePlugin
    )
    plugin1 = plugin_registry.get_plugin(AgentPluginType.EXPLOITER, PLUGIN_NAME)
    plugin2 = plugin_registry.get_plugin(AgentPluginType.EXPLOITER, PLUGIN_NAME)

    assert plugin1.__class__ == plugin2.__class__
    assert plugin1.name == plugin2.name
    assert id(plugin1) != id(plugin2)


@pytest.mark.parametrize(
    "plugin_type",
    [AgentPluginType.CREDENTIALS_COLLECTOR, AgentPluginType.EXPLOITER],
)
def test_get_plugin__loads_supported_plugin_types(
    mock_island_api_client: IIslandAPIClient,
    mock_plugin_factories: Dict[AgentPluginType, IPluginFactory],
    plugin_registry: PluginRegistry,
    plugin_type,
):
    agent_plugin = agent_plugin_of_type(plugin_type)
    mock_island_api_client.get_agent_plugin = MagicMock(return_value=agent_plugin)

    plugin_registry.get_plugin(plugin_type, PLUGIN_NAME)

    assert mock_plugin_factories[plugin_type].create.called


@pytest.mark.parametrize(
    "plugin_type",
    [AgentPluginType.FINGERPRINTER],
)
def test_get_plugin__raises_error_for_unsupported_plugin_types(
    plugin_registry: PluginRegistry, plugin_type
):
    with pytest.raises(UnknownPluginError):
        plugin_registry.get_plugin(plugin_type, PLUGIN_NAME)
