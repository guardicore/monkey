import pytest
import requests
import requests_mock

from infection_monkey.network.relay.utils import find_server

SERVER_1 = "1.1.1.1:12312"
SERVER_2 = "2.2.2.2:4321"
SERVER_3 = "3.3.3.3:3142"
SERVER_4 = "4.4.4.4:5000"


servers = [SERVER_1, SERVER_2, SERVER_3, SERVER_4]


@pytest.mark.parametrize(
    "expected_server,server_response_pairs",
    [
        (
            None,
            [
                (SERVER_1, {"exc": requests.exceptions.ConnectionError}),
                (SERVER_2, {"exc": requests.exceptions.ConnectionError}),
                (SERVER_3, {"exc": requests.exceptions.ConnectionError}),
                (SERVER_4, {"exc": requests.exceptions.ConnectionError}),
            ],
        ),
        (
            SERVER_2,
            [
                (SERVER_1, {"exc": requests.exceptions.ConnectionError}),
                (SERVER_2, {"text": ""}),
                (SERVER_3, {"text": ""}),
                (SERVER_4, {"text": ""}),
            ],
        ),
    ],
)
def test_find_server(expected_server, server_response_pairs):
    with requests_mock.Mocker() as mock:
        for server, response in server_response_pairs:
            mock.get(f"https://{server}/api?action=is-up", **response)

        assert find_server(servers) is expected_server
