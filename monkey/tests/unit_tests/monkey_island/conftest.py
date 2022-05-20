import os
from collections.abc import Callable

import flask_restful
import pytest
from flask import Flask

import monkey_island
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


def mock_flask_resource_manager(container):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test_key"

    api = flask_restful.Api(app)
    api.representations = {"application/json": output_json}

    monkey_island.cc.app.init_app_url_rules(app)
    flask_resource_manager = monkey_island.cc.app.FlaskDIWrapper(api, container)

    return flask_resource_manager
