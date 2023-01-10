import os
import re
import uuid
from datetime import timedelta
from typing import Iterable, Set, Type

import flask_restful
from flask import Flask, Response, send_from_directory
from werkzeug.exceptions import NotFound

from common import DIContainer
from monkey_island.cc.database import database, mongo
from monkey_island.cc.resources import (
    AgentBinaries,
    AgentConfiguration,
    AgentConfigurationSchema,
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
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.auth import Authenticate, Register, RegistrationStatus, init_jwt
from monkey_island.cc.resources.exploitations.monkey_exploitation import MonkeyExploitation
from monkey_island.cc.resources.island_mode import IslandMode
from monkey_island.cc.resources.local_run import LocalRun
from monkey_island.cc.resources.ransomware_report import RansomwareReport
from monkey_island.cc.resources.root import Root
from monkey_island.cc.resources.security_report import SecurityReport
from monkey_island.cc.resources.version import Version
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.services.representations import output_json

HOME_FILE = "index.html"
AUTH_EXPIRATION_TIME = timedelta(minutes=30)


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


def init_app_config(app, mongo_url):
    app.config["MONGO_URI"] = mongo_url

    # See https://flask-jwt-extended.readthedocs.io/en/stable/options
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = AUTH_EXPIRATION_TIME
    # Invalidate the signature of JWTs if the server process restarts. This avoids the edge case
    # of getting a JWT,
    # deciding to reset credentials and then still logging in with the old JWT.
    app.config["JWT_SECRET_KEY"] = str(uuid.uuid4())

    # By default, Flask sorts keys of JSON objects alphabetically.
    # See https://flask.palletsprojects.com/en/1.1.x/config/#JSON_SORT_KEYS.
    app.config["JSON_SORT_KEYS"] = False

    app.url_map.strict_slashes = False


def init_app_services(app):
    init_jwt(app)
    mongo.init_app(app)

    with app.app_context():
        database.init()


def init_app_url_rules(app):
    app.add_url_rule("/", "serve_home", serve_home)
    app.add_url_rule("/<path:static_path>", "serve_static_file", serve_static_file)


class FlaskDIWrapper:
    class DuplicateURLError(Exception):
        pass

    url_parameter_regex = re.compile(r"<.*?:.*?>")

    def __init__(self, api: flask_restful.Api, container: DIContainer):
        self._api = api
        self._container = container
        self._reserved_urls: Set[str] = set()

    def add_resource(self, resource: Type[AbstractResource]):
        if len(resource.urls) == 0:
            raise ValueError(f"Resource {resource.__name__} has no defined URLs")

        self._reserve_urls(resource.urls)

        # enforce our rule that URLs should not contain a trailing slash
        for url in resource.urls:
            if url.endswith("/"):
                raise ValueError(
                    f"Resource {resource.__name__} has an invalid URL: A URL "
                    "should not have a trailing slash."
                )
        dependencies = self._container.resolve_dependencies(resource)
        self._api.add_resource(resource, *resource.urls, resource_class_args=dependencies)

    def _reserve_urls(self, urls: Iterable[str]):
        for url in map(FlaskDIWrapper._format_url, urls):
            if url in self._reserved_urls:
                raise FlaskDIWrapper.DuplicateURLError(f"URL {url} has already been registered!")

            self._reserved_urls.add(url)

    @staticmethod
    def _format_url(url: str):
        new_url = url.strip("/")
        return FlaskDIWrapper.url_parameter_regex.sub("<PARAMETER_PLACEHOLDER>", new_url)


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
    api.add_resource(AgentConfiguration)
    api.add_resource(AgentConfigurationSchema)
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


def init_rpc_endpoints(api: FlaskDIWrapper):
    api.add_resource(ResetAgentConfiguration)
    api.add_resource(ClearSimulationData)
    api.add_resource(TerminateAllAgents)


def init_app(mongo_url: str, container: DIContainer):
    """
    Simple docstirng for init_app

    :param mongo_url: A url
    :param container: Dependency injection container
    """
    app = Flask(__name__)

    api = flask_restful.Api(app)
    api.representations = {"application/json": output_json}

    init_app_config(app, mongo_url)
    init_app_services(app)
    init_app_url_rules(app)

    flask_resource_manager = FlaskDIWrapper(api, container)
    init_api_resources(flask_resource_manager)

    return app
