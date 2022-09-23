from typing import Callable, Optional

import pytest
import requests_mock

from common.agent_event_serializers import AgentEventSerializerRegistry
from common.types import SocketAddress
from infection_monkey.island_api_client import (
    HTTPIslandAPIClientFactory,
    IIslandAPIClient,
    IslandAPIConnectionError,
)
from infection_monkey.network.relay.utils import IslandAPISearchResult, find_available_island_apis

SERVER_1 = SocketAddress(ip="1.1.1.1", port=12312)
SERVER_2 = SocketAddress(ip="2.2.2.2", port=4321)
SERVER_3 = SocketAddress(ip="3.3.3.3", port=3142)
SERVER_4 = SocketAddress(ip="4.4.4.4", port=5000)


servers = [SERVER_1, SERVER_2, SERVER_3, SERVER_4]


@pytest.fixture
def island_api_client_factory():
    return HTTPIslandAPIClientFactory(AgentEventSerializerRegistry())


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

        available_apis = find_available_island_apis(servers, island_api_client_factory)

        assert len(available_apis) == len(server_response_pairs)

        for result in available_apis:
            if result.server in expected_available_servers:
                assert result.client is not None
            else:
                assert result.client is None


def test_find_available_island_apis__preserves_input_order(island_api_client_factory):
    available_servers = [SERVER_2, SERVER_3]

    with requests_mock.Mocker() as mock:
        mock.get(f"https://{SERVER_1}/api?action=is-up", exc=IslandAPIConnectionError)
        for server in available_servers:
            mock.get(f"https://{server}/api?action=is-up", text="")
        available_apis = find_available_island_apis(servers, island_api_client_factory)

        for index in range(len(servers)):
            assert available_apis[index].server == servers[index]


def _is_none(value) -> bool:
    return value is None


def _is_island_client(value) -> bool:
    return isinstance(value, IIslandAPIClient)


def _assert_server_and_predicate(
    result: IslandAPISearchResult,
    server: SocketAddress,
    predicate: Callable[[Optional[IIslandAPIClient]], bool],
):
    assert result.server == server
    assert predicate(result.client)


def test_find_available_island_apis__multiple_successes(island_api_client_factory):
    available_servers = [SERVER_2, SERVER_3]
    with requests_mock.Mocker() as mock:
        mock.get(f"https://{SERVER_1}/api?action=is-up", exc=IslandAPIConnectionError)
        for server in available_servers:
            mock.get(f"https://{server}/api?action=is-up", text="")

        available_apis = find_available_island_apis(servers, island_api_client_factory)

        _assert_server_and_predicate(available_apis[0], SERVER_1, _is_none)
        _assert_server_and_predicate(available_apis[1], SERVER_2, _is_island_client)
        _assert_server_and_predicate(available_apis[2], SERVER_3, _is_island_client)
        _assert_server_and_predicate(available_apis[3], SERVER_4, _is_none)
