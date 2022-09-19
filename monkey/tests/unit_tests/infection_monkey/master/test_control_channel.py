from unittest.mock import MagicMock

import pytest

from infection_monkey.i_control_channel import IslandCommunicationError
from infection_monkey.island_api_client import (
    IIslandAPIClient,
    IslandAPIConnectionError,
    IslandAPITimeoutError,
)
from infection_monkey.master.control_channel import ControlChannel


@pytest.fixture
def island_api_client() -> IIslandAPIClient:
    client = MagicMock()
    return client


@pytest.fixture
def control_channel(island_api_client) -> ControlChannel:
    return ControlChannel("server", "agent-id", island_api_client)


def test_control_channel__register_agent(control_channel, island_api_client):
    control_channel.register_agent()
    assert island_api_client.register_agent.called_once()


def test_control_channel__register_agent_raises_on_connection_error(
    control_channel, island_api_client
):
    island_api_client.register_agent.side_effect = IslandAPIConnectionError()

    with pytest.raises(IslandCommunicationError):
        control_channel.register_agent()


def test_control_channel__register_agent_raises_on_timeout_error(
    control_channel, island_api_client
):
    island_api_client.register_agent.side_effect = IslandAPITimeoutError()

    with pytest.raises(IslandCommunicationError):
        control_channel.register_agent()
