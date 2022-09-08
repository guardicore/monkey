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
    "expected_server,connection_error_servers,do_nothing_servers",
    [(None, servers, []), (SERVER_2, [SERVER_1], [SERVER_2, SERVER_3, SERVER_4])],
)
def test_find_server(expected_server, connection_error_servers, do_nothing_servers):
    with requests_mock.Mocker() as mock:
        for server in connection_error_servers:
            mock.get(f"https://{server}/api?action=is-up", exc=requests.exceptions.ConnectionError)
        for server in do_nothing_servers:
            mock.get(f"https://{server}/api?action=is-up", text="")

        assert find_server(servers) is expected_server
