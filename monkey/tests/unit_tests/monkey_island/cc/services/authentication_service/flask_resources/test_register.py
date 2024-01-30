from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from flask import Response

from common.common_consts.token_keys import ACCESS_TOKEN_KEY_NAME, TOKEN_TTL_KEY_NAME
from monkey_island.cc.services.authentication_service.authentication_facade import (
    AuthenticationFacade,
)
from monkey_island.cc.services.authentication_service.flask_resources.register import Register

USERNAME = "testuser"
PASSWORD = "test_password"
TEST_REQUEST = f'{{"username": "{USERNAME}", "password": "{PASSWORD}"}}'
FLASK_REGISTER_IMPORT = (
    "monkey_island.cc.services.authentication_service.flask_resources.register.register"
)
REGISTER_RESPONSE_DATA = (
    b'{"response": {"user": {"authentication_token": "abcdefg"}, "csrf_token": "hijklmnop"}}'
)
REGISTER_RESPONSE = Response(
    response=REGISTER_RESPONSE_DATA,
    status=HTTPStatus.OK,
    mimetype="application/json",
)


@pytest.fixture
def make_registration_request(flask_client):
    url = Register.urls[0]

    def inner(request_body):
        return flask_client.post(url, data=request_body, follow_redirects=True)

    return inner


def test_register_failed(
    monkeypatch, make_registration_request, mock_authentication_facade: AuthenticationFacade
):
    response = make_registration_request("{}")

    mock_authentication_facade.handle_successful_registration.assert_not_called()
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_register__already_registered(
    monkeypatch, make_registration_request, mock_authentication_facade: AuthenticationFacade
):
    mock_authentication_facade.needs_registration.return_value = False

    response = make_registration_request("{}")

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json["response"]["errors"]


def test_register_successful(
    monkeypatch, make_registration_request, mock_authentication_facade: AuthenticationFacade
):
    monkeypatch.setattr(FLASK_REGISTER_IMPORT, lambda: REGISTER_RESPONSE)

    response = make_registration_request(TEST_REQUEST)

    assert response.status_code == HTTPStatus.OK
    token_ttl_sec = response.json["response"]["user"][TOKEN_TTL_KEY_NAME]
    assert isinstance(token_ttl_sec, int)
    assert token_ttl_sec > 0
    assert ACCESS_TOKEN_KEY_NAME in response.json["response"]["user"]
    mock_authentication_facade.handle_successful_registration.assert_called_with(USERNAME, PASSWORD)


@pytest.mark.parametrize(
    "register_response",
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
def test_register_invalid_request(
    monkeypatch,
    register_response,
    make_registration_request,
    mock_authentication_facade: AuthenticationFacade,
):
    monkeypatch.setattr(FLASK_REGISTER_IMPORT, lambda: register_response)

    response = make_registration_request(b"{}")

    assert response.status_code == HTTPStatus.BAD_REQUEST
    mock_authentication_facade.handle_successful_registration.assert_not_called()


def test_register_error(
    monkeypatch, make_registration_request, mock_authentication_facade: AuthenticationFacade
):
    monkeypatch.setattr(FLASK_REGISTER_IMPORT, lambda: REGISTER_RESPONSE)

    mock_authentication_facade.handle_successful_registration = MagicMock(side_effect=Exception())

    response = make_registration_request(TEST_REQUEST)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_register_invalid_username(
    monkeypatch, make_registration_request, mock_authentication_facade: AuthenticationFacade
):
    mock_authentication_facade.handle_successful_registration = MagicMock(side_effect=Exception())
    invalid_username_request = (
        f'{{"username": "constrainted-username123", "password": "{PASSWORD}"}}'
    )
    response = make_registration_request(invalid_username_request)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "response" in response.json
    assert "errors" in response.json["response"]
