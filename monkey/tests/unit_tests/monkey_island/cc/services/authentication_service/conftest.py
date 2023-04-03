from typing import Tuple
from unittest.mock import MagicMock

import pytest
from flask import Flask
from flask_restful import Api
from flask_security import Security
from tests.unit_tests.monkey_island.conftest import (
    init_mock_app,
    init_mock_datastore,
    init_mock_security_app,
)

from monkey_island.cc.services.authentication_service import register_resources
from monkey_island.cc.services.authentication_service.authentication_facade import (
    AuthenticationFacade,
)

REFRESH_TOKEN = "refresh_token"


@pytest.fixture
def mock_authentication_facade():
    mock_service = MagicMock(spec=AuthenticationFacade)
    mock_service.generate_refresh_token = MagicMock()
    mock_service.generate_refresh_token.return_value = REFRESH_TOKEN

    return mock_service


@pytest.fixture
def build_flask_client(mock_authentication_facade):
    def inner():
        return get_mock_auth_app(mock_authentication_facade).test_client()

    return inner


def get_mock_auth_app(authentication_facade: AuthenticationFacade):
    app, api = init_mock_security_app()
    register_resources(api, authentication_facade)
    return app


@pytest.fixture
def flask_client(build_flask_client, mock_authentication_facade):
    with build_flask_client() as flask_client:
        yield flask_client


def build_app() -> Tuple[Flask, Api]:
    app, api = init_mock_app()
    user_datastore = init_mock_datastore()
    app.security = Security(app, user_datastore)
    return app, api
