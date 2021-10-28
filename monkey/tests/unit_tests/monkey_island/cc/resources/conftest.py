import flask_jwt_extended
import flask_restful
import pytest
from flask import Flask

import monkey_island.cc.app
import monkey_island.cc.resources.auth.auth
import monkey_island.cc.resources.island_mode
from monkey_island.cc.services.representations import output_json


@pytest.fixture(scope="session")
def flask_client(monkeypatch_session):
    monkeypatch_session.setattr(flask_jwt_extended, "verify_jwt_in_request", lambda: None)

    with mock_init_app().test_client() as client:
        yield client


def mock_init_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test_key"

    api = flask_restful.Api(app)
    api.representations = {"application/json": output_json}

    monkey_island.cc.app.init_app_url_rules(app)
    monkey_island.cc.app.init_api_resources(api)

    flask_jwt_extended.JWTManager(app)

    return app
