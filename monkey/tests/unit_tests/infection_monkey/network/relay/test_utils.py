import pytest
import requests_mock
from tests.data_for_tests.otp import OTP

from common.agent_event_serializers import AgentEventSerializerRegistry
from common.types import SocketAddress
from infection_monkey.island_api_client import (
    HTTPIslandAPIClientFactory,
    IIslandAPIClient,
    IslandAPIConnectionError,
)
from infection_monkey.network.relay.utils import find_available_island_apis

SERVER_1 = SocketAddress(ip="1.1.1.1", port=12312)
SERVER_2 = SocketAddress(ip="2.2.2.2", port=4321)
SERVER_3 = SocketAddress(ip="3.3.3.3", port=3142)
SERVER_4 = SocketAddress(ip="4.4.4.4", port=5000)


servers = [SERVER_1, SERVER_2, SERVER_3, SERVER_4]


@pytest.fixture
def island_api_client_factory():
    return HTTPIslandAPIClientFactory(AgentEventSerializerRegistry(), OTP)


@pytest.mark.parametrize(
    "expected_available_servers, server_response_pairs",
    [
        ([], [(server, {"exc": IslandAPIConnectionError}) for server in servers]),
        (
            servers[1:],
            [(SERVER_1, {"exc": IslandAPIConnectionError})]
            + [(server, {"text": ""}) for server in servers[1:]],  # type: ignore[dict-item]
        ),
    ],
)
def test_find_available_island_apis(
    expected_available_servers, server_response_pairs, island_api_client_factory
):
    with requests_mock.Mocker() as mock:
        for server, response in server_response_pairs:
            mock.get(f"https://{server}/api?action=is-up", **response)
            mock.post(f"https://{server}/api/agent-otp-login", json={"token": "fake-token"})

        available_apis = find_available_island_apis(servers, island_api_client_factory)

        assert len(available_apis) == len(server_response_pairs)

        for server, island_api_client in available_apis.items():
            if server in expected_available_servers:
                assert island_api_client is not None
            else:
                assert island_api_client is None


def test_find_available_island_apis__multiple_successes(island_api_client_factory):
    available_servers = [SERVER_2, SERVER_3]
    with requests_mock.Mocker() as mock:
        mock.get(f"https://{SERVER_1}/api?action=is-up", exc=IslandAPIConnectionError)
        mock.post(f"https://{SERVER_1}/api/agent-otp-login", json={"token": "fake-token"})
        for server in available_servers:
            mock.post(f"https://{server}/api/agent-otp-login", json={"token": "fake-token"})
            mock.get(f"https://{server}/api?action=is-up", text="")

        available_apis = find_available_island_apis(servers, island_api_client_factory)

        assert available_apis[SERVER_1] is None
        assert available_apis[SERVER_4] is None
        for server in available_servers:
            assert isinstance(available_apis[server], IIslandAPIClient)
