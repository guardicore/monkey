from http import HTTPStatus

import pytest

from monkey_island.cc.services.authentication_service.authentication_facade import (
    AuthenticationFacade,
)
from monkey_island.cc.services.authentication_service.flask_resources.token import Token
from monkey_island.cc.services.authentication_service.flask_resources.utils import (
    REFRESH_TOKEN_KEY_NAME,
)

REQUEST_AUTHENTICATION_TOKEN = "my_authentication_token"
REQUEST_REFRESH_TOKEN = "my_refresh_token"
REQUEST = {REFRESH_TOKEN_KEY_NAME: REQUEST_REFRESH_TOKEN}

NEW_AUTHENTICATION_TOKEN = "new_authentication_token"
NEW_REFRESH_TOKEN = "new_refresh_token"


@pytest.fixture
def request_token(flask_client):
    url = Token.urls[0]

    def inner(request_body):
        return flask_client.post(url, json=request_body, follow_redirects=True)

    return inner


def test_token__provides_refreshed_token(
    request_token, mock_authentication_facade: AuthenticationFacade
):
    mock_authentication_facade.generate_new_token_pair.return_value = (
        NEW_AUTHENTICATION_TOKEN,
        NEW_REFRESH_TOKEN,
    )

    response = request_token(REQUEST)

    assert response.status_code == HTTPStatus.OK
    assert response.json["response"]["user"]["refresh_token"] == NEW_REFRESH_TOKEN
    assert response.json["response"]["user"]["access_token"] == NEW_AUTHENTICATION_TOKEN


def test_token__fails_if_refresh_token_is_invalid(
    request_token, mock_authentication_facade: AuthenticationFacade
):
    mock_authentication_facade.generate_new_token_pair.side_effect = Exception()

    response = request_token(REQUEST)

    assert response.status_code == HTTPStatus.BAD_REQUEST
