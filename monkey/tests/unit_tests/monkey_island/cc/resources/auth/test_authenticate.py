from flask import Response
from unittest.mock import MagicMock

import pytest

from monkey_island.cc.resources.auth import Authenticate

USERNAME = "test_user"
PASSWORD = "test_password"
TEST_REQUEST = f'{{"username": "{USERNAME}", "password": "{PASSWORD}"}}'


@pytest.fixture
def make_auth_request(flask_client):
    url = Authenticate.urls[0]

    def inner(request_body):
        return flask_client.post(url, data=request_body, follow_redirects=True)

    return inner


def test_credential_parsing(make_auth_request, mock_authentication_service, monkeypatch):
    monkeypatch.setattr(
        "monkey_island.cc.resources.auth.authenticate.login",
        lambda: Response(
            status=200,
        ),
    )

    make_auth_request(TEST_REQUEST)
    mock_authentication_service.unlock_repository_encryptor.assert_called_with(USERNAME, PASSWORD)


def test_empty_credentials(make_auth_request, mock_authentication_service):
    make_auth_request("{}")
    mock_authentication_service.unlock_repository_encryptor.assert_not_called()


def test_authentication_successful(make_auth_request, monkeypatch):
    monkeypatch.setattr(
        "monkey_island.cc.resources.auth.authenticate.login",
        lambda: Response(
            status=200,
        ),
    )

    response = make_auth_request(TEST_REQUEST)

    assert response.status_code == 200


def test_authentication_failure(make_auth_request, mock_authentication_service, monkeypatch):
    monkeypatch.setattr(
        "monkey_island.cc.resources.auth.authenticate.login",
        lambda: Response(
            status=400,
        ),
    )

    response = make_auth_request(TEST_REQUEST)

    assert response.status_code == 400
    mock_authentication_service.unlock_repository_encryptor.assert_not_called()


def test_authentication_error(make_auth_request, mock_authentication_service):
    mock_authentication_service.unlock_repository_encryptor = MagicMock(side_effect=Exception())

    response = make_auth_request(TEST_REQUEST)

    assert "access_token" not in response.json
    assert response.status_code == 500
