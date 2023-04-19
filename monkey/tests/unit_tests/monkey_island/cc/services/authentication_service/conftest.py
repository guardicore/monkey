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

from monkey_island.cc.services.authentication_service import IOTPGenerator, register_resources
from monkey_island.cc.services.authentication_service.authentication_facade import (
    AuthenticationFacade,
)


@pytest.fixture
def mock_authentication_facade():
    maf = MagicMock(spec=AuthenticationFacade)
    maf.token_ttl_sec = 123

    return maf


@pytest.fixture
def mock_otp_generator() -> IOTPGenerator:
    mog = MagicMock(spec=IOTPGenerator)

    return mog


@pytest.fixture
def build_flask_client(
    mock_authentication_facade: AuthenticationFacade,
    mock_otp_generator: IOTPGenerator,
):
    def inner():
        return get_mock_auth_app(mock_authentication_facade, mock_otp_generator).test_client()

    return inner


def get_mock_auth_app(authentication_facade: AuthenticationFacade, otp_generator: IOTPGenerator):
    app, api = init_mock_security_app()
    register_resources(api, authentication_facade, otp_generator, MagicMock())
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
