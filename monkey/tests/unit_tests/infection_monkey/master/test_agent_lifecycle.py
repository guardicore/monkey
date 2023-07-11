from typing import Optional
from unittest.mock import MagicMock

import pytest

from common import AgentSignals
from infection_monkey.island_api_client import (
    IIslandAPIClient,
    IslandAPIConnectionError,
    IslandAPIRequestError,
    IslandAPIRequestFailedError,
    IslandAPITimeoutError,
)
from infection_monkey.master import AgentLifecycle

SERVER = "server"
API_ERRORS = [
    IslandAPIConnectionError,
    IslandAPIRequestError,
    IslandAPIRequestFailedError,
    IslandAPITimeoutError,
]


@pytest.fixture
def island_api_client() -> IIslandAPIClient:
    client = MagicMock(spec=IIslandAPIClient)
    return client


@pytest.fixture
def agent_lifecycle(island_api_client: IIslandAPIClient) -> AgentLifecycle:
    return AgentLifecycle(island_api_client)


@pytest.mark.parametrize("signal_time,expected_should_stop", [(1663950115, True), (None, False)])
def test_should_agent_stop(
    agent_lifecycle,
    island_api_client,
    signal_time: Optional[int],
    expected_should_stop: bool,
):
    island_api_client.get_agent_signals = MagicMock(
        return_value=AgentSignals(terminate=signal_time)  # type: ignore[arg-type]
    )
    assert agent_lifecycle.should_agent_stop() is expected_should_stop


@pytest.mark.parametrize("api_error", API_ERRORS)
def test_should_agent_stop__raises_error(agent_lifecycle, island_api_client, api_error):
    island_api_client.get_agent_signals.side_effect = api_error()

    with pytest.raises(api_error):
        agent_lifecycle.should_agent_stop()
