import os
import uuid
from datetime import timedelta
from typing import Type

import flask_restful
from flask import Flask, Response, send_from_directory
from werkzeug.exceptions import NotFound

from common import DIContainer
from monkey_island.cc.database import database, mongo
from monkey_island.cc.resources.agent_controls import StopAgentCheck, StopAllAgents
from monkey_island.cc.resources.attack.attack_report import AttackReport
from monkey_island.cc.resources.auth.auth import Authenticate, init_jwt
from monkey_island.cc.resources.auth.registration import Registration
from monkey_island.cc.resources.blackbox.clear_caches import ClearCaches
from monkey_island.cc.resources.blackbox.log_blackbox_endpoint import LogBlackboxEndpoint
from monkey_island.cc.resources.blackbox.monkey_blackbox_endpoint import MonkeyBlackboxEndpoint
from monkey_island.cc.resources.blackbox.telemetry_blackbox_endpoint import (
    TelemetryBlackboxEndpoint,
)
from monkey_island.cc.resources.configuration_export import ConfigurationExport
from monkey_island.cc.resources.configuration_import import ConfigurationImport
from monkey_island.cc.resources.edge import Edge
from monkey_island.cc.resources.exploitations.manual_exploitation import ManualExploitation
from monkey_island.cc.resources.exploitations.monkey_exploitation import MonkeyExploitation
from monkey_island.cc.resources.island_configuration import IslandConfiguration
from monkey_island.cc.resources.island_logs import IslandLog
from monkey_island.cc.resources.island_mode import IslandMode
from monkey_island.cc.resources.local_run import LocalRun
from monkey_island.cc.resources.log import Log
from monkey_island.cc.resources.monkey import Monkey
from monkey_island.cc.resources.monkey_download import MonkeyDownload
from monkey_island.cc.resources.netmap import NetMap
from monkey_island.cc.resources.node import Node
from monkey_island.cc.resources.node_states import NodeStates
from monkey_island.cc.resources.pba_file_download import PBAFileDownload
from monkey_island.cc.resources.pba_file_upload import FileUpload
from monkey_island.cc.resources.propagation_credentials import PropagationCredentials
from monkey_island.cc.resources.ransomware_report import RansomwareReport
from monkey_island.cc.resources.remote_run import RemoteRun
from monkey_island.cc.resources.root import Root
from monkey_island.cc.resources.security_report import SecurityReport
from monkey_island.cc.resources.telemetry import Telemetry
from monkey_island.cc.resources.telemetry_feed import TelemetryFeed
from monkey_island.cc.resources.version_update import VersionUpdate
from monkey_island.cc.resources.zero_trust.finding_event import ZeroTrustFindingEvent
from monkey_island.cc.resources.zero_trust.zero_trust_report import ZeroTrustReport
from monkey_island.cc.server_utils.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.server_utils.custom_json_encoder import CustomJSONEncoder
from monkey_island.cc.services.remote_run_aws import RemoteRunAwsService
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
    app.json_encoder = CustomJSONEncoder


def init_app_services(app):
    init_jwt(app)
    mongo.init_app(app)

    with app.app_context():
        database.init()

    # If running on AWS, this will initialize the instance data, which is used "later" in the
    # execution of the island.
    RemoteRunAwsService.init()


def init_app_url_rules(app):
    app.add_url_rule("/", "serve_home", serve_home)
    app.add_url_rule("/<path:static_path>", "serve_static_file", serve_static_file)


# TODO: Come up with a better name than FlaskResourceManager
class FlaskResourceManager:
    def __init__(self, api: flask_restful.Api, container: DIContainer):
        self._api = api
        self._container = container

    def add_resource(self, resource: Type[flask_restful.Resource], *urls: str):
        dependencies = self._container.resolve_dependencies(resource)
        self._api.add_resource(resource, *urls, resource_class_args=dependencies)


def init_api_resources(flask_resource_manager: FlaskResourceManager):
    flask_resource_manager.add_resource(Root, "/api")
    flask_resource_manager.add_resource(Registration, "/api/registration")
    flask_resource_manager.add_resource(Authenticate, "/api/auth")
    flask_resource_manager.add_resource(
        Monkey,
        "/api/agent",
        "/api/agent/<string:guid>",
        "/api/agent/<string:guid>/<string:config_format>",
    )
    flask_resource_manager.add_resource(LocalRun, "/api/local-monkey")
    flask_resource_manager.add_resource(
        Telemetry, "/api/telemetry", "/api/telemetry/<string:monkey_guid>"
    )

    flask_resource_manager.add_resource(IslandMode, "/api/island-mode")
    flask_resource_manager.add_resource(IslandConfiguration, "/api/configuration/island")
    flask_resource_manager.add_resource(ConfigurationExport, "/api/configuration/export")
    flask_resource_manager.add_resource(ConfigurationImport, "/api/configuration/import")
    flask_resource_manager.add_resource(
        MonkeyDownload,
        "/api/agent/download/<string:host_os>",
    )
    flask_resource_manager.add_resource(NetMap, "/api/netmap")
    flask_resource_manager.add_resource(Edge, "/api/netmap/edge")
    flask_resource_manager.add_resource(Node, "/api/netmap/node")
    flask_resource_manager.add_resource(NodeStates, "/api/netmap/node-states")

    flask_resource_manager.add_resource(SecurityReport, "/api/report/security")
    flask_resource_manager.add_resource(
        ZeroTrustReport, "/api/report/zero-trust/<string:report_data>"
    )
    flask_resource_manager.add_resource(AttackReport, "/api/report/attack")
    flask_resource_manager.add_resource(RansomwareReport, "/api/report/ransomware")
    flask_resource_manager.add_resource(ManualExploitation, "/api/exploitations/manual")
    flask_resource_manager.add_resource(MonkeyExploitation, "/api/exploitations/monkey")

    flask_resource_manager.add_resource(
        ZeroTrustFindingEvent, "/api/zero-trust/finding-event/<string:finding_id>"
    )
    flask_resource_manager.add_resource(TelemetryFeed, "/api/telemetry-feed")
    flask_resource_manager.add_resource(Log, "/api/log")
    flask_resource_manager.add_resource(IslandLog, "/api/log/island/download")

    flask_resource_manager.add_resource(
        PBAFileDownload,
        "/api/pba/download/<string:filename>",
    )
    flask_resource_manager.add_resource(
        FileUpload,
        "/api/file-upload/<string:file_type>",
        "/api/file-upload/<string:file_type>?load=<string:filename>",
        "/api/file-upload/<string:file_type>?restore=<string:filename>",
    )

    flask_resource_manager.add_resource(
        PropagationCredentials, "/api/propagation-credentials/<string:guid>"
    )
    flask_resource_manager.add_resource(RemoteRun, "/api/remote-monkey")
    flask_resource_manager.add_resource(VersionUpdate, "/api/version-update")
    flask_resource_manager.add_resource(
        StopAgentCheck, "/api/monkey-control/needs-to-stop/<int:monkey_guid>"
    )
    flask_resource_manager.add_resource(StopAllAgents, "/api/monkey-control/stop-all-agents")

    # Resources used by black box tests
    flask_resource_manager.add_resource(MonkeyBlackboxEndpoint, "/api/test/monkey")
    flask_resource_manager.add_resource(ClearCaches, "/api/test/clear-caches")
    flask_resource_manager.add_resource(LogBlackboxEndpoint, "/api/test/log")
    flask_resource_manager.add_resource(TelemetryBlackboxEndpoint, "/api/test/telemetry")


def init_app(mongo_url: str, container: DIContainer):
    app = Flask(__name__)

    api = flask_restful.Api(app)
    api.representations = {"application/json": output_json}

    init_app_config(app, mongo_url)
    init_app_services(app)
    init_app_url_rules(app)

    flask_resource_manager = FlaskResourceManager(api, container)
    init_api_resources(flask_resource_manager)

    return app
