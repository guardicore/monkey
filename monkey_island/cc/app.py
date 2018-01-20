from datetime import datetime
import bson
from bson.json_util import dumps
from flask import Flask, send_from_directory, redirect, make_response
import flask_restful
from werkzeug.exceptions import NotFound

from cc.database import mongo
from cc.resources.client_run import ClientRun
from cc.resources.monkey import Monkey
from cc.resources.local_run import LocalRun
from cc.resources.telemetry import Telemetry
from cc.resources.monkey_configuration import MonkeyConfiguration
from cc.resources.monkey_download import MonkeyDownload
from cc.resources.netmap import NetMap
from cc.resources.edge import Edge
from cc.resources.node import Node
from cc.resources.report import Report
from cc.resources.root import Root
from cc.resources.telemetry_feed import TelemetryFeed
from cc.services.config import ConfigService

__author__ = 'Barak'


def serve_static_file(static_path):
    if static_path.startswith('api/'):
        raise NotFound()
    try:
        return send_from_directory('ui/dist', static_path)
    except NotFound:
        # Because react uses various urls for same index page, this is probably the user's intention.
        return serve_home()


def serve_home():
    return serve_static_file('index.html')


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


def init_app(mongo_url):
    app = Flask(__name__)

    api = flask_restful.Api(app)
    api.representations = {'application/json': output_json}

    app.config['MONGO_URI'] = mongo_url
    mongo.init_app(app)

    with app.app_context():
        ConfigService.init_config()

    app.add_url_rule('/', 'serve_home', serve_home)
    app.add_url_rule('/<path:static_path>', 'serve_static_file', serve_static_file)

    api.add_resource(Root, '/api')
    api.add_resource(Monkey, '/api/monkey', '/api/monkey/', '/api/monkey/<string:guid>')
    api.add_resource(LocalRun, '/api/local-monkey', '/api/local-monkey/')
    api.add_resource(ClientRun, '/api/client-monkey', '/api/client-monkey/')
    api.add_resource(Telemetry, '/api/telemetry', '/api/telemetry/', '/api/telemetry/<string:monkey_guid>')
    api.add_resource(MonkeyConfiguration, '/api/configuration', '/api/configuration/')
    api.add_resource(MonkeyDownload, '/api/monkey/download', '/api/monkey/download/',
                     '/api/monkey/download/<string:path>')
    api.add_resource(NetMap, '/api/netmap', '/api/netmap/')
    api.add_resource(Edge, '/api/netmap/edge', '/api/netmap/edge/')
    api.add_resource(Node, '/api/netmap/node', '/api/netmap/node/')
    api.add_resource(Report, '/api/report', '/api/report/')
    api.add_resource(TelemetryFeed, '/api/telemetry-feed', '/api/telemetry-feed/')

    return app
