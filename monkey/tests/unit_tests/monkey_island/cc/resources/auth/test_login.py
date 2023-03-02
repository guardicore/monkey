from unittest.mock import MagicMock

import pytest
from flask import Response

from monkey_island.cc.resources.auth import Login

USERNAME = "test_user"
PASSWORD = "test_password"
TEST_REQUEST = f'{{"username": "{USERNAME}", "password": "{PASSWORD}"}}'


@pytest.fixture
def make_login_request(flask_client):
    url = Login.urls[0]

    def inner(request_body):
        return flask_client.post(url, data=request_body, follow_redirects=True)

    return inner


def test_credential_parsing(make_login_request, mock_authentication_service, monkeypatch):
    monkeypatch.setattr(
        "monkey_island.cc.resources.auth.login.login",
        lambda: Response(
            status=200,
        ),
    )

    make_login_request(TEST_REQUEST)
    mock_authentication_service.unlock_repository_encryptor.assert_called_with(USERNAME, PASSWORD)


def test_empty_credentials(make_login_request, mock_authentication_service):
    make_login_request("{}")
    mock_authentication_service.unlock_repository_encryptor.assert_not_called()


def test_login_successful(make_login_request, monkeypatch):
    monkeypatch.setattr(
        "monkey_island.cc.resources.auth.login.login",
        lambda: Response(
            status=200,
        ),
    )

    response = make_login_request(TEST_REQUEST)

    assert response.status_code == 200


def test_login_failure(make_login_request, mock_authentication_service, monkeypatch):
    monkeypatch.setattr(
        "monkey_island.cc.resources.auth.login.login",
        lambda: Response(
            status=400,
        ),
    )

    response = make_login_request(TEST_REQUEST)

    assert response.status_code == 400
    mock_authentication_service.unlock_repository_encryptor.assert_not_called()


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
    monkeypatch, login_response, make_login_request, mock_authentication_service
):
    monkeypatch.setattr("monkey_island.cc.resources.auth.login.login", lambda: login_response)

    response = make_login_request(b"{}")

    assert response.status_code == 400
    mock_authentication_service.unlock_repository_encryptor.assert_not_called()


def test_login_error(monkeypatch, make_login_request, mock_authentication_service):
    monkeypatch.setattr(
        "monkey_island.cc.resources.auth.login.login",
        lambda: Response(
            status=200,
        ),
    )
    mock_authentication_service.unlock_repository_encryptor = MagicMock(side_effect=Exception())

    response = make_login_request(TEST_REQUEST)

    assert "access_token" not in response.json
    assert response.status_code == 500
