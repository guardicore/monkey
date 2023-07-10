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
from infection_monkey.utils import should_agent_stop

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


@pytest.mark.parametrize("signal_time,expected_should_stop", [(1663950115, True), (None, False)])
def test_should_agent_stop(
    island_api_client,
    signal_time: Optional[int],
    expected_should_stop: bool,
):
    island_api_client.get_agent_signals = MagicMock(
        return_value=AgentSignals(terminate=signal_time)  # type: ignore[arg-type]
    )
    assert should_agent_stop(SERVER, island_api_client) is expected_should_stop


@pytest.mark.parametrize("api_error", API_ERRORS)
def test_should_agent_stop__raises_error(island_api_client, api_error):
    island_api_client.get_agent_signals.side_effect = api_error()

    with pytest.raises(api_error):
        should_agent_stop(SERVER, island_api_client)


def test_should_agent_stop__server_is_none(island_api_client: IIslandAPIClient):
    assert should_agent_stop(None, island_api_client)
