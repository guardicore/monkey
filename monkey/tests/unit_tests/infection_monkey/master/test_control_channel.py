from unittest.mock import MagicMock

import pytest

from infection_monkey.i_control_channel import IslandCommunicationError
from infection_monkey.island_api_client import (
    IIslandAPIClient,
    IslandAPIConnectionError,
    IslandAPIRequestError,
    IslandAPIRequestFailedError,
    IslandAPITimeoutError,
)
from infection_monkey.master.control_channel import ControlChannel

SERVER = "server"
AGENT_ID = "agent"
CONTROL_CHANNEL_API_ERRORS = [
    IslandAPIConnectionError,
    IslandAPIRequestError,
    IslandAPIRequestFailedError,
    IslandAPITimeoutError,
]


@pytest.fixture
def island_api_client() -> IIslandAPIClient:
    client = MagicMock()
    return client


@pytest.fixture
def control_channel(island_api_client) -> ControlChannel:
    return ControlChannel(SERVER, AGENT_ID, island_api_client)


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


def test_control_channel__should_agent_stop(control_channel, island_api_client):
    control_channel.should_agent_stop()
    assert island_api_client.should_agent_stop.called_once()


def test_control_channel__should_agent_stop_raises_on_connection_error(
    control_channel, island_api_client
):
    island_api_client.should_agent_stop.side_effect = IslandAPIConnectionError()

    with pytest.raises(IslandCommunicationError):
        control_channel.should_agent_stop()


def test_control_channel__should_agent_stop_raises_on_timeout_error(
    control_channel, island_api_client
):
    island_api_client.should_agent_stop.side_effect = IslandAPITimeoutError()

    with pytest.raises(IslandCommunicationError):
        control_channel.should_agent_stop()


def test_control_channel__should_agent_stop_raises_on_request_error(
    control_channel, island_api_client
):
    island_api_client.should_agent_stop.side_effect = IslandAPIRequestError()

    with pytest.raises(IslandCommunicationError):
        control_channel.should_agent_stop()


def test_control_channel__should_agent_stop_raises_on_request_failed_error(
    control_channel, island_api_client
):
    island_api_client.should_agent_stop.side_effect = IslandAPIRequestFailedError()

    with pytest.raises(IslandCommunicationError):
        control_channel.should_agent_stop()


def test_control_channel__get_config(control_channel, island_api_client):
    control_channel.get_config()
    assert island_api_client.get_config.called_once()


@pytest.mark.parametrize("api_error", CONTROL_CHANNEL_API_ERRORS)
def test_control_channel__get_config_raises_error(control_channel, island_api_client, api_error):
    island_api_client.get_config.side_effect = api_error()

    with pytest.raises(IslandCommunicationError):
        control_channel.get_config()


def test_control_channel__get_credentials_for_propagation(control_channel, island_api_client):
    control_channel.get_credentials_for_propagation()
    assert island_api_client.get_credentials_for_propagation.called_once()


@pytest.mark.parametrize("api_error", CONTROL_CHANNEL_API_ERRORS)
def test_control_channel__get_credentials_for_propagation_raises_error(
    control_channel, island_api_client, api_error
):
    island_api_client.get_credentials_for_propagation.side_effect = api_error()

    with pytest.raises(IslandCommunicationError):
        control_channel.get_credentials_for_propagation()
