from http import HTTPStatus

import pytest
from monkeytypes import Token

from common.common_consts.token_keys import ACCESS_TOKEN_KEY_NAME, TOKEN_TTL_KEY_NAME
from monkey_island.cc.services.authentication_service.authentication_facade import (
    AuthenticationFacade,
)
from monkey_island.cc.services.authentication_service.flask_resources.refresh_authentication_token import (  # noqa: E501
    RefreshAuthenticationToken,
)

NEW_AUTHENTICATION_TOKEN = Token("new_authentication_token")
TOKEN_TTL_SEC = 123


@pytest.fixture
def request_token(flask_client):
    url = RefreshAuthenticationToken.urls[0]

    def inner():
        return flask_client.post(url, follow_redirects=True)

    return inner


def test_token__provides_refreshed_token(
    request_token, mock_authentication_facade: AuthenticationFacade
):
    mock_authentication_facade.refresh_user_token.return_value = (
        NEW_AUTHENTICATION_TOKEN,
        TOKEN_TTL_SEC,
    )

    response = request_token()

    assert response.status_code == HTTPStatus.OK
    assert (
        response.json["response"]["user"][ACCESS_TOKEN_KEY_NAME]
        == NEW_AUTHENTICATION_TOKEN.get_secret_value()
    )
    assert response.json["response"]["user"][TOKEN_TTL_KEY_NAME] == TOKEN_TTL_SEC


def test_token__fails_if_refresh_token_is_invalid(
    request_token, mock_authentication_facade: AuthenticationFacade
):
    mock_authentication_facade.refresh_user_token.side_effect = Exception()

    response = request_token()

    assert response.status_code == HTTPStatus.BAD_REQUEST
