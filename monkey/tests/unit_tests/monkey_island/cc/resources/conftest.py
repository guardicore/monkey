from unittest.mock import MagicMock

import flask_jwt_extended
import flask_restful
import pytest
from flask import Flask

import monkey_island.cc.app
import monkey_island.cc.resources.auth.auth
import monkey_island.cc.resources.island_mode
from monkey_island.cc.services.representations import output_json


@pytest.fixture
def flask_client(monkeypatch_session):
    monkeypatch_session.setattr(flask_jwt_extended, "verify_jwt_in_request", lambda: None)

    container = MagicMock()
    container.resolve_dependencies.return_value = []

    with mock_init_app(container).test_client() as client:
        yield client


@pytest.fixture
def build_flask_client(monkeypatch_session):
    def inner(container):
        monkeypatch_session.setattr(flask_jwt_extended, "verify_jwt_in_request", lambda: None)

        return mock_init_app(container).test_client()

    return inner


def mock_init_app(container):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test_key"

    api = flask_restful.Api(app)
    api.representations = {"application/json": output_json}

    monkey_island.cc.app.init_app_url_rules(app)
    flask_resource_manager = monkey_island.cc.app.FlaskDIWrapper(api, container)
    monkey_island.cc.app.init_api_resources(flask_resource_manager)

    flask_jwt_extended.JWTManager(app)

    return app
