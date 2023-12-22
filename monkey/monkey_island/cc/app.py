import os
from pathlib import Path

import flask_restful
from flask import Flask, Response, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from ophidian import DIContainer
from werkzeug.exceptions import NotFound

from monkey_island.cc.flask_utils import FlaskDIWrapper
from monkey_island.cc.mongo_consts import MONGO_URL
from monkey_island.cc.resources import (
    AgentEvents,
    AgentHeartbeat,
    Agents,
    AgentSignals,
    ClearSimulationData,
    Machines,
    Nodes,
    PropagationCredentials,
    RemoteRun,
    ReportGenerationStatus,
    ResetAgentConfiguration,
    TerminateAllAgents,
)
from monkey_island.cc.resources.exploitations.monkey_exploitation import MonkeyExploitation
from monkey_island.cc.resources.local_run import LocalRun
from monkey_island.cc.resources.ransomware_report import RansomwareReport
from monkey_island.cc.resources.root import Root
from monkey_island.cc.resources.security_report import SecurityReport
from monkey_island.cc.resources.version import Version
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.services import (
    register_agent_binary_resources,
    register_agent_configuration_resources,
    register_agent_plugin_resources,
    setup_authentication,
    setup_log_service,
)
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


def init_app_config(app):
    # By default, Flask sorts keys of JSON objects alphabetically.
    # See https://flask.palletsprojects.com/en/1.1.x/config/#JSON_SORT_KEYS.
    app.config["JSON_SORT_KEYS"] = False

    mongo_url = "".join(MONGO_URL.rpartition("/")[0])
    app.config["RATELIMIT_HEADERS_ENABLED"] = True
    app.config["RATELIMIT_STRATEGY"] = "moving-window"
    app.config["RATELIMIT_STORAGE_URI"] = mongo_url

    app.url_map.strict_slashes = False


def init_app_url_rules(app):
    app.add_url_rule("/", "serve_home", serve_home)
    app.add_url_rule("/<path:static_path>", "serve_static_file", serve_static_file)


def init_api_resources(api: FlaskDIWrapper):
    init_restful_endpoints(api)
    init_rpc_endpoints(api)


def init_restful_endpoints(api: FlaskDIWrapper):
    api.add_resource(Root)

    api.add_resource(Agents)
    api.add_resource(LocalRun)

    api.add_resource(Machines)

    api.add_resource(SecurityReport)
    api.add_resource(RansomwareReport)
    api.add_resource(MonkeyExploitation)

    api.add_resource(AgentEvents)
    api.add_resource(AgentSignals)

    api.add_resource(PropagationCredentials)
    api.add_resource(RemoteRun)
    api.add_resource(Version)

    api.add_resource(Nodes)

    api.add_resource(ReportGenerationStatus)

    api.add_resource(AgentHeartbeat)

    register_agent_configuration_resources(api)
    register_agent_binary_resources(api)
    register_agent_plugin_resources(api)


def init_rpc_endpoints(api: FlaskDIWrapper):
    api.add_resource(ResetAgentConfiguration)
    api.add_resource(ClearSimulationData)
    api.add_resource(TerminateAllAgents)


def init_app(
    container: DIContainer,
    data_dir: Path,
):
    """
    Simple docstring for init_app

    :param mongo_url: A url
    :param container: Dependency injection container
    """
    app = Flask(__name__)

    api = flask_restful.Api(app)
    api.representations = {"application/json": output_json}

    init_app_config(app)
    init_app_url_rules(app)

    limiter = Limiter(
        get_remote_address,
        app=app,
    )
    setup_authentication(api, app, container, data_dir, limiter)
    setup_log_service(api, container, data_dir)
    flask_resource_manager = FlaskDIWrapper(api, container)
    init_api_resources(flask_resource_manager)

    return app
