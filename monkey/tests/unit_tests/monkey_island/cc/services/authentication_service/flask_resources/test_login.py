from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from flask import Response

from common.common_consts.token_keys import ACCESS_TOKEN_KEY_NAME, TOKEN_TTL_KEY_NAME
from monkey_island.cc.services.authentication_service.authentication_facade import (
    AuthenticationFacade,
)
from monkey_island.cc.services.authentication_service.flask_resources.login import Login

USERNAME = "test_user"
PASSWORD = "test_password"
TEST_REQUEST = f'{{"username": "{USERNAME}", "password": "{PASSWORD}"}}'
FLASK_LOGIN_IMPORT = "monkey_island.cc.services.authentication_service.flask_resources.login.login"
LOGIN_RESPONSE_DATA = (
    b'{"response": {"user": {"authentication_token": "abcdefg"}, "csrf_token": "hijklmnop"}}'
)
LOGIN_RESPONSE = Response(
    response=LOGIN_RESPONSE_DATA,
    status=HTTPStatus.OK,
    mimetype="application/json",
)


@pytest.fixture
def make_login_request(flask_client):
    url = Login.urls[0]

    def inner(request_body):
        return flask_client.post(url, data=request_body, follow_redirects=True)

    return inner


def test_credential_parsing(
    monkeypatch, make_login_request, mock_authentication_facade: AuthenticationFacade
):
    monkeypatch.setattr(FLASK_LOGIN_IMPORT, lambda: LOGIN_RESPONSE)

    make_login_request(TEST_REQUEST)
    mock_authentication_facade.handle_successful_login.assert_called_with(USERNAME, PASSWORD)


def test_empty_credentials(make_login_request, mock_authentication_facade: AuthenticationFacade):
    make_login_request("{}")
    mock_authentication_facade.handle_successful_login.assert_not_called()


def test_login_successful(make_login_request, monkeypatch):
    monkeypatch.setattr(FLASK_LOGIN_IMPORT, lambda: LOGIN_RESPONSE)

    response = make_login_request(TEST_REQUEST)

    assert response.status_code == HTTPStatus.OK
    token_ttl_sec = response.json["response"]["user"][TOKEN_TTL_KEY_NAME]
    assert isinstance(token_ttl_sec, int)
    assert token_ttl_sec > 0
    assert ACCESS_TOKEN_KEY_NAME in response.json["response"]["user"]


def test_login_failure(
    monkeypatch, make_login_request, mock_authentication_facade: AuthenticationFacade
):
    monkeypatch.setattr(
        FLASK_LOGIN_IMPORT,
        lambda: Response(
            status=HTTPStatus.BAD_REQUEST,
        ),
    )

    response = make_login_request(TEST_REQUEST)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    mock_authentication_facade.handle_successful_login.assert_not_called()


@pytest.mark.parametrize(
    "login_response",
    [
        1111,
        "adfasdf",
        None,
        True,
        MagicMock(side_effect=Exception),
        {"some_value": "other_value"},
        b"bogus_bytes",
        b"{bogus}",
        ["item1", 123, "something"],
    ],
)
def test_login_invalid_request(
    monkeypatch,
    login_response,
    make_login_request,
    mock_authentication_facade: AuthenticationFacade,
):
    monkeypatch.setattr(FLASK_LOGIN_IMPORT, lambda: login_response)

    response = make_login_request(b"{}")

    assert response.status_code == HTTPStatus.BAD_REQUEST
    mock_authentication_facade.handle_successful_login.assert_not_called()


def test_login_error(
    monkeypatch, make_login_request, mock_authentication_facade: AuthenticationFacade
):
    monkeypatch.setattr(FLASK_LOGIN_IMPORT, lambda: LOGIN_RESPONSE)
    mock_authentication_facade.handle_successful_login = MagicMock(side_effect=Exception())

    response = make_login_request(TEST_REQUEST)

    assert "access_token" not in response.json
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
