import flask_restful
import pytest
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_security import MongoEngineUserDatastore, Security

import monkey_island
from monkey_island.cc.models import Role, User
from monkey_island.cc.services.representations import output_json


def init_mock_security_app(db_name):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "test_key"
    app.config["SECURITY_PASSWORD_SALT"] = b"somethingsaltyandniceandgood"
    # Our test emails/domain isn't necessarily valid
    app.config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {"check_deliverability": False}
    # Make this plaintext for most tests - reduces unit test time by 50%
    app.config["SECURITY_PASSWORD_HASH"] = "plaintext"
    app.config["TESTING"] = True
    app.config["MONGO_URI"] = "mongomock://localhost"
    api = flask_restful.Api(app)
    api.representations = {"application/json": output_json}

    monkey_island.cc.app.init_app_url_rules(app)

    db = MongoEngine()
    db.disconnect(alias="default")
    db.connect(db_name, host="mongomock://localhost")

    user_datastore = MongoEngineUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)
    return app


@pytest.fixture(scope="function")
def mock_flask_app():
    from common.utils.code_utils import insecure_generate_random_string

    db_name = insecure_generate_random_string(8)
    app = init_mock_security_app(db_name)

    with app.app_context():
        yield app
