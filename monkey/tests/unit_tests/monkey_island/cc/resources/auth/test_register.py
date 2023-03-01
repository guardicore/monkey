import json
from unittest.mock import MagicMock

import pytest
from flask import Response

from monkey_island.cc.resources.auth import Register

USERNAME = "test_user"
PASSWORD = "test_password"
TEST_REQUEST = f'{{"username": "{USERNAME}", "password": "{PASSWORD}"}}'


@pytest.fixture
def make_auth_request(flask_client):
    url = Register.urls[0]

    def inner(request_body):
        return flask_client.post(url, data=request_body, follow_redirects=True)

    return inner


def test_register_failed(monkeypatch, make_auth_request, mock_authentication_service):
    monkeypatch.setattr(
        "monkey_island.cc.resources.auth.register.register",
        lambda: Response(
            status=400,
        ),
    )
    response = make_auth_request("{}")

    mock_authentication_service.reset_island.assert_not_called()
    mock_authentication_service.reset_repository_encryptor.assert_not_called()
    assert response.status_code == 400


def test_register_successful(monkeypatch, make_auth_request, mock_authentication_service):
    monkeypatch.setattr(
        "monkey_island.cc.resources.auth.register.register",
        lambda: Response(
            status=200,
        ),
    )

    response = make_auth_request(TEST_REQUEST)

    assert response.status_code == 200
    mock_authentication_service.reset_island_data.assert_called_once()
    mock_authentication_service.reset_repository_encryptor.assert_called_once()


def test_register_error(monkeypatch, make_auth_request, mock_authentication_service):
    monkeypatch.setattr(
        "monkey_island.cc.resources.auth.register.register",
        lambda: Response(status=200),
    )

    mock_authentication_service.reset_island_data = MagicMock(side_effect=Exception())

    response = make_auth_request(TEST_REQUEST)

    assert "csrf_token" not in json.loads(response.data)
    assert response.status_code == 500
