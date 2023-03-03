from unittest.mock import MagicMock

import flask_security
import pytest
from tests.common import StubDIContainer
from tests.monkey_island import OpenErrorFileRepository
from tests.unit_tests.monkey_island.conftest import init_mock_app

import monkey_island.cc.app
import monkey_island.cc.resources.auth
import monkey_island.cc.resources.island_mode
from monkey_island.cc.repositories import IFileRepository


@pytest.fixture
def flask_client(monkeypatch_session):
    monkeypatch_session.setattr(flask_security.decorators, "_check_token", lambda: True)

    container = MagicMock()
    container.resolve_dependencies.return_value = []

    with get_mock_app(container).test_client() as client:
        yield client


@pytest.fixture
def build_flask_client(monkeypatch_session):
    monkeypatch_session.setattr(flask_security.decorators, "_check_token", lambda: True)

    def inner(container):
        return get_mock_app(container).test_client()

    return inner


def get_mock_app(container):
    app, api = init_mock_app()
    flask_resource_manager = monkey_island.cc.app.FlaskDIWrapper(api, container)
    monkey_island.cc.app.init_api_resources(flask_resource_manager)

    return app


@pytest.fixture
def open_error_flask_client(build_flask_client):
    container = StubDIContainer()
    container.register(IFileRepository, OpenErrorFileRepository)

    with build_flask_client(container) as flask_client:
        yield flask_client
