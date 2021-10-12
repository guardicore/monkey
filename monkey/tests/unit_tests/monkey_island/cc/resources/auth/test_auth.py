import re
from unittest.mock import MagicMock

import pytest

USERNAME = "test_user"
PASSWORD = "test_password"
TEST_REQUEST = f'{{"username": "{USERNAME}", "password": "{PASSWORD}"}}'


@pytest.fixture
def mock_authentication_service(monkeypatch):
    mock_service = MagicMock()
    mock_service.authenticate = MagicMock()

    monkeypatch.setattr("monkey_island.cc.resources.auth.auth.AuthenticationService", mock_service)

    return mock_service


@pytest.fixture
def make_auth_request(flask_client):
    url = "/api/auth"

    def inner(request_body):
        return flask_client.post(url, data=request_body, follow_redirects=True)

    return inner


def test_credential_parsing(make_auth_request, mock_authentication_service):
    make_auth_request(TEST_REQUEST)
    mock_authentication_service.authenticate.assert_called_with(USERNAME, PASSWORD)


def test_empty_credentials(make_auth_request, mock_authentication_service):
    make_auth_request("{}")
    mock_authentication_service.authenticate.assert_called_with("", "")


def test_authentication_successful(make_auth_request, mock_authentication_service):
    mock_authentication_service.authenticate = MagicMock(return_value=True)

    response = make_auth_request(TEST_REQUEST)

    assert response.status_code == 200
    assert response.json["error"] == ""
    assert re.match(
        r"^[a-zA-Z0-9+/=]+\.[a-zA-Z0-9+/=]+\.[a-zA-Z0-9+/=\-_]+$", response.json["access_token"]
    )


def test_authentication_failure(make_auth_request, mock_authentication_service):
    mock_authentication_service.authenticate = MagicMock(return_value=False)

    response = make_auth_request(TEST_REQUEST)

    assert "access_token" not in response.json
    assert response.status_code == 401
    assert response.json["error"] == "Invalid credentials"


def test_authentication_error(make_auth_request, mock_authentication_service):
    mock_authentication_service.authenticate = MagicMock(side_effect=Exception())

    response = make_auth_request(TEST_REQUEST)

    assert "access_token" not in response.json
    assert response.status_code == 500
