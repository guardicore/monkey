from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from flask import Response

from monkey_island.cc.services.authentication_service.account_role import AccountRole
from monkey_island.cc.services.authentication_service.authentication_facade import (
    AuthenticationFacade,
)
from monkey_island.cc.services.authentication_service.flask_resources.logout import Logout
from monkey_island.cc.services.authentication_service.user import User

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

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert not mock_authentication_facade.remove_user.called


def test_logout_successful(monkeypatch, make_logout_request):
    monkeypatch.setattr(
        FLASK_LOGOUT_IMPORT,
        lambda: Response(
            status=HTTPStatus.OK,
        ),
    )

    response = make_logout_request("")

    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "role, expect_remove_user_called",
    [(AccountRole.AGENT.name, True), (AccountRole.ISLAND_INTERFACE.name, False)],
)
def test_logout__removes_agent_user(
    monkeypatch,
    make_logout_request,
    role: AccountRole,
    expect_remove_user_called: bool,
    mock_authentication_facade: AuthenticationFacade,
):
    monkeypatch.setattr(
        FLASK_LOGOUT_IMPORT,
        lambda: Response(
            status=HTTPStatus.OK,
        ),
    )
    mock_user = MagicMock(spec=User)
    mock_user.username = "test_user"
    mock_user.has_role = lambda r: r == role
    monkeypatch.setattr(
        "monkey_island.cc.services.authentication_service.flask_resources.logout.current_user",
        mock_user,
    )

    response = make_logout_request("")

    assert response.status_code == HTTPStatus.OK
    if expect_remove_user_called:
        mock_authentication_facade.remove_user.assert_called_once_with(mock_user.username)
    else:
        assert not mock_authentication_facade.remove_user.called
