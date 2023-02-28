import re
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


def test_register_with_empty_credentials(
    monkeypatch, make_auth_request, mock_authentication_service
):
    monkeypatch.setattr(
        "flask_security.views.register",
        lambda: Response(status_code=400),
    )
    response = make_auth_request("{}")
    mock_authentication_service.reset_island.assert_not_called()

    assert response.status_code == 400


# def test_authentication_successful(make_auth_request, mock_authentication_service):
#    response = make_auth_request(TEST_REQUEST)

#    assert response.status_code == 200
#    assert re.match(
#        r"^[a-zA-Z0-9+/=]+\.[a-zA-Z0-9+/=]+\.[a-zA-Z0-9+/=\-_]+$", response.json["csrf_token"]
#    )


# def test_authentication_failure(make_auth_request, mock_authentication_service):
#
#    response = make_auth_request(TEST_REQUEST)
#
#    assert "access_token" not in response.json
#    assert response.status_code == 401
#    assert response.json["error"] == "Invalid credentials"


# def test_authentication_error(make_auth_request, mock_authentication_service):
#    mock_authentication_service.authenticate = MagicMock(side_effect=Exception())
#
#    response = make_auth_request(TEST_REQUEST)
#
#    assert "access_token" not in response.json
#    assert response.status_code == 500
