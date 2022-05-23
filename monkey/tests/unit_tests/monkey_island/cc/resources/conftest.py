from unittest.mock import MagicMock

import flask_jwt_extended
import pytest
from tests.unit_tests.monkey_island.conftest import init_mock_app

import monkey_island.cc.app
import monkey_island.cc.resources.auth.auth
import monkey_island.cc.resources.island_mode


@pytest.fixture
def flask_client(monkeypatch_session):
    monkeypatch_session.setattr(flask_jwt_extended, "verify_jwt_in_request", lambda: None)

    container = MagicMock()
    container.resolve_dependencies.return_value = []

    with get_mock_app(container).test_client() as client:
        yield client


@pytest.fixture
def build_flask_client(monkeypatch_session):
    def inner(container):
        monkeypatch_session.setattr(flask_jwt_extended, "verify_jwt_in_request", lambda: None)

        return get_mock_app(container).test_client()

    return inner


def get_mock_app(container):
    app, api = init_mock_app()
    flask_resource_manager = monkey_island.cc.app.FlaskDIWrapper(api, container)
    monkey_island.cc.app.init_api_resources(flask_resource_manager)

    flask_jwt_extended.JWTManager(app)

    return app
