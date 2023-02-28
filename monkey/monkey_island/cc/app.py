import os
from pathlib import Path

import flask_restful
from flask import Flask, Response, send_from_directory
from flask_mongoengine import MongoEngine
from flask_security import ConfirmRegisterForm, MongoEngineUserDatastore, Security
from werkzeug.exceptions import NotFound
from wtforms import PasswordField, StringField, validators

from common import DIContainer
from monkey_island.cc.models import Role, User
from monkey_island.cc.flask_utils import FlaskDIWrapper
from monkey_island.cc.resources import (
    AgentBinaries,
    AgentEvents,
    AgentHeartbeat,
    AgentLogs,
    AgentPlugins,
    AgentPluginsManifest,
    Agents,
    AgentSignals,
    ClearSimulationData,
    IslandLog,
    Machines,
    Nodes,
    PropagationCredentials,
    RemoteRun,
    ReportGenerationStatus,
    ResetAgentConfiguration,
    TerminateAllAgents,
)
from monkey_island.cc.resources.auth import Authenticate, Register, RegistrationStatus
from monkey_island.cc.resources.exploitations.monkey_exploitation import MonkeyExploitation
from monkey_island.cc.resources.island_mode import IslandMode
from monkey_island.cc.resources.local_run import LocalRun
from monkey_island.cc.resources.ransomware_report import RansomwareReport
from monkey_island.cc.resources.root import Root
from monkey_island.cc.resources.security_report import SecurityReport
from monkey_island.cc.resources.version import Version
from monkey_island.cc.server_utils import generate_flask_security_configuration
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.services import register_agent_configuration_resources
from monkey_island.cc.services.representations import output_json
from monkey_island.cc.setup.mongo.mongo_setup import MONGO_DB_HOST, MONGO_DB_NAME, MONGO_DB_PORT

HOME_FILE = "index.html"


def serve_static_file(static_path):
    if static_path.startswith("api/"):
        raise NotFound()
    try:
        return send_from_directory(os.path.join(MONKEY_ISLAND_ABS_PATH, "cc/ui/dist"), static_path)
    except NotFound:
        # Because react uses various urls for same index page, this is probably the user's
        # intention.
        if static_path == HOME_FILE:
            flask_restful.abort(
                Response(
                    "Page not found. Make sure you ran the npm script and the cwd is "
                    "monkey\\monkey.",
                    500,
                )
            )
        return serve_home()


def serve_home():
    return serve_static_file(HOME_FILE)


def setup_authentication(app, data_dir):
    flask_security_config = generate_flask_security_configuration(data_dir)

    # TODO: After we switch to token base authentication investigate the purpose
    # of `SECRET_KEY` and `SECURITY_PASSWORD_SALT`, take into consideration
    # the discussion https://github.com/guardicore/monkey/pull/3006#discussion_r1116944571
    app.config["SECRET_KEY"] = flask_security_config["secret_key"]
    app.config["SECURITY_PASSWORD_SALT"] = flask_security_config["password_salt"]
    app.config["SECURITY_USERNAME_ENABLE"] = True
    app.config["SECURITY_USERNAME_REQUIRED"] = True
    app.config["SECURITY_REGISTERABLE"] = True
    app.config["WTF_CSRF_CHECK_DEFAULT"] = False
    app.config["SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS"] = True
    app.config["SECURITY_SEND_REGISTER_EMAIL"] = False

    # The database object needs to be created after we configure the flask application
    db = MongoEngine(app)

    class CustomConfirmRegisterForm(ConfirmRegisterForm):
        # Flask-Security doesn't let you register without an email field
        email = StringField("Email", default="dummy@dummy.com")
        password = PasswordField(
            "Password",
            [validators.DataRequired(), validators.Length(min=1, max=25)],
        )

    user_datastore = MongoEngineUserDatastore(db, User, Role)

    app.security = Security(app, user_datastore, confirm_register_form=CustomConfirmRegisterForm)


def init_app_config(app, mongo_url, data_dir: Path):
    app.config["MONGO_URI"] = mongo_url
    app.config["MONGODB_SETTINGS"] = [
        {
            "db": MONGO_DB_NAME,
            "host": MONGO_DB_HOST,
            "port": MONGO_DB_PORT,
        }
    ]

    # By default, Flask sorts keys of JSON objects alphabetically.
    # See https://flask.palletsprojects.com/en/1.1.x/config/#JSON_SORT_KEYS.
    app.config["JSON_SORT_KEYS"] = False

    app.url_map.strict_slashes = False

    setup_authentication(app, data_dir)


def init_app_url_rules(app):
    app.add_url_rule("/", "serve_home", serve_home)
    app.add_url_rule("/<path:static_path>", "serve_static_file", serve_static_file)


def init_api_resources(api: FlaskDIWrapper):
    init_restful_endpoints(api)
    init_rpc_endpoints(api)


def init_restful_endpoints(api: FlaskDIWrapper):
    api.add_resource(Root)
    api.add_resource(Register)
    api.add_resource(RegistrationStatus)
    api.add_resource(Authenticate)
    api.add_resource(Agents)
    api.add_resource(LocalRun)

    api.add_resource(IslandMode)
    api.add_resource(AgentBinaries)
    api.add_resource(AgentPlugins)
    api.add_resource(AgentPluginsManifest)
    api.add_resource(Machines)

    api.add_resource(SecurityReport)
    api.add_resource(RansomwareReport)
    api.add_resource(MonkeyExploitation)

    api.add_resource(AgentLogs)
    api.add_resource(IslandLog)

    api.add_resource(AgentEvents)
    api.add_resource(AgentSignals)

    api.add_resource(PropagationCredentials)
    api.add_resource(RemoteRun)
    api.add_resource(Version)

    api.add_resource(Nodes)

    api.add_resource(ReportGenerationStatus)

    api.add_resource(AgentHeartbeat)

    register_agent_configuration_resources(api)


def init_rpc_endpoints(api: FlaskDIWrapper):
    api.add_resource(ResetAgentConfiguration)
    api.add_resource(ClearSimulationData)
    api.add_resource(TerminateAllAgents)


def init_app(mongo_url: str, container: DIContainer, data_dir: Path):
    """
    Simple docstirng for init_app

    :param mongo_url: A url
    :param container: Dependency injection container
    """
    app = Flask(__name__)

    api = flask_restful.Api(app)
    api.representations = {"application/json": output_json}

    init_app_config(app, mongo_url, data_dir)
    init_app_url_rules(app)

    flask_resource_manager = FlaskDIWrapper(api, container)
    init_api_resources(flask_resource_manager)

    return app
