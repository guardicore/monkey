import pytest
import requests
import requests_mock
from monkeytypes import SocketAddress

from infection_monkey.network.relay.utils import find_available_island_apis

SERVER_1 = SocketAddress(ip="1.1.1.1", port=12312)
SERVER_2 = SocketAddress(ip="2.2.2.2", port=4321)
SERVER_3 = SocketAddress(ip="3.3.3.3", port=3142)
SERVER_4 = SocketAddress(ip="4.4.4.4", port=5000)


servers = [SERVER_1, SERVER_2, SERVER_3, SERVER_4]


@pytest.mark.parametrize(
    "expected_available_servers, server_response_pairs",
    [
        ([], [(server, {"exc": requests.exceptions.RequestException}) for server in servers]),
        (
            servers[1:],
            [(SERVER_1, {"exc": requests.exceptions.HTTPError})]
            + [(server, {"text": ""}) for server in servers[1:]],  # type: ignore[dict-item]
        ),
    ],
)
def test_find_available_island_apis(expected_available_servers, server_response_pairs):
    with requests_mock.Mocker() as mock:
        for server, response in server_response_pairs:
            mock.get(f"https://{server}/api?action=is-up", **response)

        island_api_statuses = find_available_island_apis(servers)

        assert len(island_api_statuses) == len(server_response_pairs)

        for server, reachable in island_api_statuses.items():
            if server in expected_available_servers:
                assert reachable
            else:
                assert not reachable


def test_find_available_island_apis__multiple_successes():
    available_servers = [SERVER_2, SERVER_3]
    with requests_mock.Mocker() as mock:
        mock.get(f"https://{SERVER_1}/api?action=is-up", exc=requests.exceptions.ConnectTimeout)
        mock.get(f"https://{SERVER_4}/api?action=is-up", exc=requests.exceptions.InvalidURL)
        for server in available_servers:
            mock.get(f"https://{server}/api?action=is-up", text="")

        island_api_statuses = find_available_island_apis(servers)

        assert not island_api_statuses[SERVER_1]
        assert not island_api_statuses[SERVER_4]
        for server in available_servers:
            assert island_api_statuses[server]
