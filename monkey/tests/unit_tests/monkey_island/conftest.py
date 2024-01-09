import os
import re
from collections.abc import Callable
from typing import Set, Tuple, Type

import flask_restful
import mongomock
import pytest
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_security import MongoEngineUserDatastore, Security
from monkeytoolbox import insecure_generate_random_string

import monkey_island
from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services.authentication_service import AccountRole
from monkey_island.cc.services.authentication_service.flask_resources.login import Login
from monkey_island.cc.services.authentication_service.flask_resources.register import Register
from monkey_island.cc.services.authentication_service.role import Role
from monkey_island.cc.services.authentication_service.user import User
from monkey_island.cc.services.representations import output_json


@pytest.fixture(scope="module")
def server_configs_dir(data_for_tests_dir):
    return os.path.join(data_for_tests_dir, "server_configs")


@pytest.fixture
def create_empty_tmp_file(tmpdir: str) -> Callable:
    def inner(file_name: str):
        new_file = os.path.join(tmpdir, file_name)
        with open(new_file, "w"):
            pass

        return new_file

    return inner


def init_mock_security_app() -> Tuple[Flask, flask_restful.Api]:
    app, api = init_mock_app()
    user_datastore = init_mock_datastore()

    agent_role = user_datastore.find_or_create_role(name=AccountRole.AGENT.name)
    island_role = user_datastore.find_or_create_role(name=AccountRole.ISLAND_INTERFACE.name)
    app.security = Security(app, user_datastore)
    ds = app.security.datastore
    with app.app_context():
        ds.create_user(
            email="unittest@me.com",
            username="test",
            password="password",
            roles=[agent_role, island_role],
        )
        ds.commit()

    set_current_user(app, ds, "unittest@me.com")

    return app, api


def init_mock_datastore() -> MongoEngineUserDatastore:
    db = MongoEngine()
    db.disconnect(alias="default")
    db_name = insecure_generate_random_string(8)
    db.connect(db_name, mongo_client_class=mongomock.MongoClient, uuidRepresentation="pythonLegacy")

    return MongoEngineUserDatastore(db, User, Role)


def init_mock_app() -> Tuple[Flask, flask_restful.Api]:
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "test_key"
    app.config["SECURITY_PASSWORD_SALT"] = b"somethingsaltyandniceandgood"
    # Our test emails/domain isn't necessarily valid
    app.config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {"check_deliverability": False}
    # Make this plaintext for most tests - reduces unit test time by 50%
    app.config["SECURITY_PASSWORD_HASH"] = "plaintext"
    app.config["SECURITY_SEND_REGISTER_EMAIL"] = False

    # According to https://flask.palletsprojects.com/en/2.2.x/config/#TESTING,
    # setting 'TESTING' results in exceptions being propagated instead of
    # letting the app catch and handle them.
    # Our UT suite consists of tests that check the error handling of the app, which is
    # why we don't want the exceptions to be propagated. To do this, we're setting
    # 'PROPAGATE_EXCEPTIONS' to False.
    # https://flask.palletsprojects.com/en/2.2.x/config/#PROPAGATE_EXCEPTIONS
    app.config["TESTING"] = True
    app.config["PROPAGATE_EXCEPTIONS"] = False

    app.config["MONGO_URI"] = "mongodb://some_host"
    app.config["WTF_CSRF_ENABLED"] = False

    api = flask_restful.Api(app)
    api.representations = {"application/json": output_json}

    monkey_island.cc.app.init_app_url_rules(app)
    return app, api


def set_current_user(app, ds, email):
    """Set up so that when request is received,
    the token will cause 'user' to be made the current_user
    """

    def token_cb(request):
        if Register.urls[0] in request.url or Login.urls[0] in request.url:
            return
        return ds.find_user(email=email)

    app.security.login_manager.request_loader(token_cb)


def mock_flask_resource_manager(container):
    _, api = init_mock_security_app()
    flask_resource_manager = monkey_island.cc.app.FlaskDIWrapper(api, container)

    return flask_resource_manager


def get_url_for_resource(resource: Type[AbstractResource], **kwargs):
    chosen_url = None
    for url in resource.urls:
        if _get_url_keywords(url) == set(kwargs.keys()):
            chosen_url = url
    if not chosen_url:
        raise Exception(
            f"Resource {resource} doesn't contain a url that matches {kwargs} keywords."
        )

    for key, value in kwargs.items():
        reg_pattern = f"<.*:{key}>"
        chosen_url = re.sub(pattern=reg_pattern, repl=value, string=chosen_url)

    return chosen_url


def _get_url_keywords(url: str) -> Set[str]:
    # Match pattern <something:keyword>, but only put "keyword" in a group
    reg_pattern = "(?:<.*?:)(.*?)(?:>)"
    reg_matches = re.finditer(reg_pattern, url)
    return set([match.groups()[0] for match in reg_matches])
