from unittest.mock import MagicMock
from uuid import UUID

import pytest
import requests_mock
from agent_plugins.payloads.cryptojacker.src.bitcoin_mining_network_traffic_simulator import (
    BitcoinMiningNetworkTrafficSimulator,
)
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout

from common.event_queue import IAgentEventPublisher
from common.types import SocketAddress

SERVER = SocketAddress(ip="127.0.0.1", port=9999)
SERVER_URL = f"http://{SERVER}"
AGENT_ID = UUID("80988359-a1cd-42a2-9b47-5b94b37cd673")

CONNECTION_CONTEXT_ERROR = ConnectionError()
READ_TIMEOUT_ERROR = ReadTimeout()
READ_TIMEOUT_ERROR.__context__ = ConnectionResetError()
CONNECTION_CONTEXT_ERROR.__context__ = READ_TIMEOUT_ERROR


CONNECTION_NO_RESET_ERROR = ConnectionError()
GENERAL_EXCEPTION = Exception()
GENERAL_EXCEPTION.__context__ = AttributeError()
CONNECTION_NO_RESET_ERROR.__context__ = GENERAL_EXCEPTION


@pytest.fixture
def request_mock_instance():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def agent_event_publisher():
    return MagicMock(spec=IAgentEventPublisher)


@pytest.fixture
def bitcoin_mining_network_traffic_simulator(
    agent_event_publisher: IAgentEventPublisher, request_mock_instance
):
    return BitcoinMiningNetworkTrafficSimulator(
        island_server_address=SERVER, agent_id=AGENT_ID, agent_event_publisher=agent_event_publisher
    )


@pytest.mark.parametrize(
    "initial_error, expected_call_count",
    [(ConnectTimeout, 0), (ConnectionError, 0), (ReadTimeout, 1), (ConnectionResetError, 1)],
)
def test_bitcoin_mining_request__error_handling(
    request_mock_instance,
    bitcoin_mining_network_traffic_simulator: BitcoinMiningNetworkTrafficSimulator,
    agent_event_publisher: IAgentEventPublisher,
    initial_error,
    expected_call_count,
):
    request_mock_instance.post(SERVER_URL, exc=initial_error)
    bitcoin_mining_network_traffic_simulator.send_bitcoin_mining_request()
    assert agent_event_publisher.publish.call_count == expected_call_count


@pytest.mark.parametrize(
    "initial_error, expected_call_count",
    [(ConnectionError(), 0), (CONNECTION_NO_RESET_ERROR, 0), (CONNECTION_CONTEXT_ERROR, 1)],
)
def test_bitcoin_mining_request__connection_error_handling(
    request_mock_instance,
    bitcoin_mining_network_traffic_simulator: BitcoinMiningNetworkTrafficSimulator,
    agent_event_publisher: IAgentEventPublisher,
    initial_error,
    expected_call_count,
):
    request_mock_instance.post(SERVER_URL, exc=initial_error)
    bitcoin_mining_network_traffic_simulator.send_bitcoin_mining_request()
    assert agent_event_publisher.publish.call_count == expected_call_count
