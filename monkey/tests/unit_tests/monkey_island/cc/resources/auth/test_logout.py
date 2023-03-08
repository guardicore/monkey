import pytest
from flask import Response

from monkey_island.cc.resources.auth import Logout

USERNAME = "test_user"
PASSWORD = "test_password"
TEST_REQUEST = f'{{"username": "{USERNAME}", "password": "{PASSWORD}"}}'


@pytest.fixture
def make_logout_request(flask_client):
    url = Logout.urls[0]

    def inner(request_body):
        return flask_client.post(url, data=request_body, follow_redirects=True)

    return inner


@pytest.mark.parametrize(
    "logout_response",
    [
        "adfasdf",
        None,
        {"some_value": "other_value"},
        b"bogus_bytes",
        b"{bogus}",
    ],
)
def test_logout_failed(
    monkeypatch, make_logout_request, mock_authentication_service, logout_response
):
    monkeypatch.setattr("monkey_island.cc.resources.auth.logout.logout", lambda: logout_response)
    response = make_logout_request(TEST_REQUEST)

    mock_authentication_service.handle_successful_logout.assert_not_called()
    assert response.status_code == 400


def test_logout_successful(monkeypatch, make_logout_request, mock_authentication_service):
    monkeypatch.setattr(
        "monkey_island.cc.resources.auth.logout.logout",
        lambda: Response(
            status=200,
        ),
    )

    response = make_logout_request("")

    assert response.status_code == 200
    mock_authentication_service.handle_successful_logout.assert_called_once()
