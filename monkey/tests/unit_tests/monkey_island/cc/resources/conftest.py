import flask_jwt_extended
import flask_restful
import mongoengine
import pytest
from flask import Flask

import monkey_island.cc.app
import monkey_island.cc.resources.auth.auth
import monkey_island.cc.resources.island_mode
from monkey_island.cc.models.island_mode_model import IslandMode
from monkey_island.cc.services.representations import output_json


# We can't scope to module, because monkeypatch is a function scoped decorator.
# Potential solutions: https://github.com/pytest-dev/pytest/issues/363#issuecomment-406536200 or
# https://stackoverflow.com/questions/53963822/python-monkeypatch-setattr-with-pytest-fixture-at-module-scope
@pytest.fixture(scope="function")
def flask_client(monkeypatch):
    monkeypatch.setattr(flask_jwt_extended, "verify_jwt_in_request", lambda: None)

    with mock_init_app().test_client() as client:
        yield client


def mock_init_app():
    app = Flask(__name__)

    api = flask_restful.Api(app)
    api.representations = {"application/json": output_json}

    monkey_island.cc.app.init_app_url_rules(app)
    monkey_island.cc.app.init_api_resources(api)

    return app


@pytest.fixture(scope="module", autouse=True)
def fake_mongo():
    mongoengine.disconnect()
    mongoengine.connect("mongoenginetest", host="mongomock://localhost")


@pytest.fixture(scope="function")
def uses_database():
    IslandMode.objects().delete()
