from http import HTTPStatus

import pytest
from flask import Response

from monkey_island.cc.resources.auth import Logout
from monkey_island.cc.services import AuthenticationService

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
    monkeypatch,
    logout_response,
    make_logout_request,
    mock_authentication_service: AuthenticationService,
):
    monkeypatch.setattr("monkey_island.cc.resources.auth.logout.logout", lambda: logout_response)
    response = make_logout_request(TEST_REQUEST)

    mock_authentication_service.handle_successful_logout.assert_not_called()
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_logout_successful(
    monkeypatch, make_logout_request, mock_authentication_service: AuthenticationService
):
    monkeypatch.setattr(
        "monkey_island.cc.resources.auth.logout.logout",
        lambda: Response(
            status=HTTPStatus.OK,
        ),
    )

    response = make_logout_request("")

    assert response.status_code == HTTPStatus.OK
    mock_authentication_service.handle_successful_logout.assert_called_once()
