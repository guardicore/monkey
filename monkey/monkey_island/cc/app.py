import os
from pathlib import Path

import flask_restful
from flask import Flask, Response, send_from_directory
from flask_mongoengine import MongoEngine
from flask_security import MongoEngineUserDatastore, Security
from werkzeug.exceptions import NotFound

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


def init_app_config(app, mongo_url, data_dir: Path):
    db = MongoEngine(app)
    app.config["MONGO_URI"] = mongo_url
    app.config["MONGODB_SETTINGS"] = [
        {
            "db": "monkeyisland",
            "host": "localhost",
            "port": 27017,
            "alias": "flask-security",
        }
    ]

    flask_security_config = generate_flask_security_configuration(data_dir)

    app.config["SECRET_KEY"] = flask_security_config["secret_key"]
    app.config["SECURITY_PASSWORD_SALT"] = flask_security_config["password_salt"]

    # By default, Flask sorts keys of JSON objects alphabetically.
    # See https://flask.palletsprojects.com/en/1.1.x/config/#JSON_SORT_KEYS.
    app.config["JSON_SORT_KEYS"] = False

    app.url_map.strict_slashes = False

    # Setup Flask-Security
    user_datastore = MongoEngineUserDatastore(db, User, Role)
    _ = Security(app, user_datastore)


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
