from http import HTTPStatus

import pytest
from flask import Response

from monkey_island.cc.services.authentication_service.authentication_facade import (
    AuthenticationFacade,
)
from monkey_island.cc.services.authentication_service.flask_resources.logout import Logout

USERNAME = "test_user"
PASSWORD = "test_password"
TEST_REQUEST = f'{{"username": "{USERNAME}", "password": "{PASSWORD}"}}'
FLASK_LOGOUT_IMPORT = (
    "monkey_island.cc.services.authentication_service.flask_resources.logout.logout"
)


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
    mock_authentication_facade: AuthenticationFacade,
):
    monkeypatch.setattr(FLASK_LOGOUT_IMPORT, lambda: logout_response)
    response = make_logout_request(TEST_REQUEST)

    mock_authentication_facade.handle_successful_logout.assert_not_called()
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_logout_successful(
    monkeypatch, make_logout_request, mock_authentication_facade: AuthenticationFacade
):
    monkeypatch.setattr(
        FLASK_LOGOUT_IMPORT,
        lambda: Response(
            status=HTTPStatus.OK,
        ),
    )

    response = make_logout_request("")

    assert response.status_code == HTTPStatus.OK
    mock_authentication_facade.handle_successful_logout.assert_called_once()
