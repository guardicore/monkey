from typing import Tuple

from flask import Flask
from flask_restful import Api
from flask_security import Security
from tests.unit_tests.monkey_island.conftest import init_mock_app, init_mock_datastore

USER_EMAIL = "unittest@me.com"


def build_app() -> Tuple[Flask, Api]:
    app, api = init_mock_app()
    user_datastore = init_mock_datastore()
    app.security = Security(app, user_datastore)
    return app, api
