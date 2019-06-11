import os
import uuid
from datetime import datetime

import bson
import flask_restful
from bson.json_util import dumps
from flask import Flask, send_from_directory, make_response, Response
from werkzeug.exceptions import NotFound

from monkey_island.cc.auth import init_jwt
from monkey_island.cc.database import mongo, database
from monkey_island.cc.environment.environment import env
from monkey_island.cc.resources.client_run import ClientRun
from monkey_island.cc.resources.edge import Edge
from monkey_island.cc.resources.local_run import LocalRun
from monkey_island.cc.resources.log import Log
from monkey_island.cc.resources.island_logs import IslandLog
from monkey_island.cc.resources.monkey import Monkey
from monkey_island.cc.resources.monkey_configuration import MonkeyConfiguration
from monkey_island.cc.resources.island_configuration import IslandConfiguration
from monkey_island.cc.resources.monkey_download import MonkeyDownload
from monkey_island.cc.resources.netmap import NetMap
from monkey_island.cc.resources.node import Node
from monkey_island.cc.resources.remote_run import RemoteRun
from monkey_island.cc.resources.report import Report
from monkey_island.cc.resources.root import Root
from monkey_island.cc.resources.telemetry import Telemetry
from monkey_island.cc.resources.telemetry_feed import TelemetryFeed
from monkey_island.cc.resources.pba_file_download import PBAFileDownload
from monkey_island.cc.resources.version_update import VersionUpdate
from monkey_island.cc.services.database import Database
from monkey_island.cc.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.services.remote_run_aws import RemoteRunAwsService
from monkey_island.cc.resources.pba_file_upload import FileUpload
from monkey_island.cc.resources.attack.attack_config import AttackConfiguration
from monkey_island.cc.resources.attack.attack_report import AttackReport

__author__ = 'Barak'


HOME_FILE = 'index.html'


def serve_static_file(static_path):
    if static_path.startswith('api/'):
        raise NotFound()
    try:
        return send_from_directory(os.path.join(MONKEY_ISLAND_ABS_PATH, 'cc/ui/dist'), static_path)
    except NotFound:
        # Because react uses various urls for same index page, this is probably the user's intention.
        if static_path == HOME_FILE:
            flask_restful.abort(
                Response("Page not found. Make sure you ran the npm script and the cwd is monkey\\monkey.", 500))
        return serve_home()


def serve_home():
    return serve_static_file(HOME_FILE)


def normalize_obj(obj):
    if '_id' in obj and not 'id' in obj:
        obj['id'] = obj['_id']
        del obj['_id']

    for key, value in obj.items():
        if type(value) is bson.objectid.ObjectId:
            obj[key] = str(value)
        if type(value) is datetime:
            obj[key] = str(value)
        if type(value) is dict:
            obj[key] = normalize_obj(value)
        if type(value) is list:
            for i in range(0, len(value)):
                if type(value[i]) is dict:
                    value[i] = normalize_obj(value[i])
    return obj


def output_json(obj, code, headers=None):
    obj = normalize_obj(obj)
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp


def init_app_config(app, mongo_url):
    app.config['MONGO_URI'] = mongo_url
    app.config['SECRET_KEY'] = str(uuid.getnode())
    app.config['JWT_AUTH_URL_RULE'] = '/api/auth'
    app.config['JWT_EXPIRATION_DELTA'] = env.get_auth_expiration_time()


def init_app_services(app):
    init_jwt(app)
    mongo.init_app(app)

    with app.app_context():
        database.init()
        Database.init_db()

    # If running on AWS, this will initialize the instance data, which is used "later" in the execution of the island.
    RemoteRunAwsService.init()


def init_app_url_rules(app):
    app.add_url_rule('/', 'serve_home', serve_home)
    app.add_url_rule('/<path:static_path>', 'serve_static_file', serve_static_file)


def init_api_resources(api):
    api.add_resource(Root, '/api')
    api.add_resource(Monkey, '/api/monkey', '/api/monkey/', '/api/monkey/<string:guid>')
    api.add_resource(LocalRun, '/api/local-monkey', '/api/local-monkey/')
    api.add_resource(ClientRun, '/api/client-monkey', '/api/client-monkey/')
    api.add_resource(Telemetry, '/api/telemetry', '/api/telemetry/', '/api/telemetry/<string:monkey_guid>')
    api.add_resource(MonkeyConfiguration, '/api/configuration', '/api/configuration/')
    api.add_resource(IslandConfiguration, '/api/configuration/island', '/api/configuration/island/')
    api.add_resource(MonkeyDownload, '/api/monkey/download', '/api/monkey/download/',
                     '/api/monkey/download/<string:path>')
    api.add_resource(NetMap, '/api/netmap', '/api/netmap/')
    api.add_resource(Edge, '/api/netmap/edge', '/api/netmap/edge/')
    api.add_resource(Node, '/api/netmap/node', '/api/netmap/node/')
    api.add_resource(Report, '/api/report', '/api/report/')
    api.add_resource(TelemetryFeed, '/api/telemetry-feed', '/api/telemetry-feed/')
    api.add_resource(Log, '/api/log', '/api/log/')
    api.add_resource(IslandLog, '/api/log/island/download', '/api/log/island/download/')
    api.add_resource(PBAFileDownload, '/api/pba/download/<string:path>')
    api.add_resource(FileUpload, '/api/fileUpload/<string:file_type>',
                     '/api/fileUpload/<string:file_type>?load=<string:filename>',
                     '/api/fileUpload/<string:file_type>?restore=<string:filename>')
    api.add_resource(RemoteRun, '/api/remote-monkey', '/api/remote-monkey/')
    api.add_resource(AttackConfiguration, '/api/attack')
    api.add_resource(AttackReport, '/api/attack/report')
    api.add_resource(VersionUpdate, '/api/version-update', '/api/version-update/')


def init_app(mongo_url):
    app = Flask(__name__)

    api = flask_restful.Api(app)
    api.representations = {'application/json': output_json}

    init_app_config(app, mongo_url)
    init_app_services(app)
    init_app_url_rules(app)
    init_api_resources(api)

    return app
