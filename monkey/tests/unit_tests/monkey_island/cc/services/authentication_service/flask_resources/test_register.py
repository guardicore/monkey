from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from flask import Response

from monkey_island.cc.services.authentication_service.authentication_service import (
    AuthenticationService,
)
from monkey_island.cc.services.authentication_service.flask_resources.register import Register

USERNAME = "test_user"
PASSWORD = "test_password"
TEST_REQUEST = f'{{"username": "{USERNAME}", "password": "{PASSWORD}"}}'
FLASK_REGISTER_IMPORT = (
    "monkey_island.cc.services.authentication_service.flask_resources.register.register"
)


@pytest.fixture
def make_registration_request(flask_client):
    url = Register.urls[0]

    def inner(request_body):
        return flask_client.post(url, data=request_body, follow_redirects=True)

    return inner


def test_register_failed(
    monkeypatch, make_registration_request, mock_authentication_service: AuthenticationService
):
    response = make_registration_request("{}")

    mock_authentication_service.handle_successful_registration.assert_not_called()
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_register_successful(
    monkeypatch, make_registration_request, mock_authentication_service: AuthenticationService
):
    monkeypatch.setattr(
        FLASK_REGISTER_IMPORT,
        lambda: Response(
            status=HTTPStatus.OK,
        ),
    )

    response = make_registration_request(TEST_REQUEST)

    assert response.status_code == HTTPStatus.OK
    mock_authentication_service.handle_successful_registration.assert_called_with(
        USERNAME, PASSWORD
    )


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
    mock_authentication_service: AuthenticationService,
):
    monkeypatch.setattr(FLASK_REGISTER_IMPORT, lambda: register_response)

    response = make_registration_request(b"{}")

    assert response.status_code == HTTPStatus.BAD_REQUEST
    mock_authentication_service.handle_successful_registration.assert_not_called()


def test_register_error(
    monkeypatch, make_registration_request, mock_authentication_service: AuthenticationService
):
    monkeypatch.setattr(
        FLASK_REGISTER_IMPORT,
        lambda: Response(status=HTTPStatus.OK),
    )

    mock_authentication_service.handle_successful_registration = MagicMock(side_effect=Exception())

    response = make_registration_request(TEST_REQUEST)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
