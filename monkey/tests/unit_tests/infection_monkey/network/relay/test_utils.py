import pytest
import requests_mock

from infection_monkey.island_api_client import IIslandAPIClient, IslandAPIConnectionError
from infection_monkey.network.relay.utils import find_available_island_apis

SERVER_1 = "1.1.1.1:12312"
SERVER_2 = "2.2.2.2:4321"
SERVER_3 = "3.3.3.3:3142"
SERVER_4 = "4.4.4.4:5000"


servers = [SERVER_1, SERVER_2, SERVER_3, SERVER_4]


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
def test_find_available_island_apis(expected_available_servers, server_response_pairs):
    with requests_mock.Mocker() as mock:
        for server, response in server_response_pairs:
            mock.get(f"https://{server}/api?action=is-up", **response)

        available_apis = find_available_island_apis(servers)

        assert len(available_apis) == len(server_response_pairs)

        for server, island_api_client in available_apis.items():
            if server in expected_available_servers:
                assert island_api_client is not None
            else:
                assert island_api_client is None


def test_find_available_island_apis__multiple_successes():
    available_servers = [SERVER_2, SERVER_3]
    with requests_mock.Mocker() as mock:
        mock.get(f"https://{SERVER_1}/api?action=is-up", exc=IslandAPIConnectionError)
        for server in available_servers:
            mock.get(f"https://{server}/api?action=is-up", text="")

        available_apis = find_available_island_apis(servers)

        assert available_apis[SERVER_1] is None
        assert available_apis[SERVER_4] is None
        for server in available_servers:
            assert isinstance(available_apis[server], IIslandAPIClient)
