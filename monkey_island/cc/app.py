from datetime import datetime

import bson
from flask import Flask, send_from_directory, redirect, make_response
import flask_restful

from cc.database import mongo
from cc.resources.monkey import Monkey
from cc.resources.local_run import LocalRun
from cc.resources.telemetry import Telemetry
from cc.resources.new_config import NewConfig
from cc.resources.monkey_download import MonkeyDownload
from cc.resources.netmap import NetMap
from cc.resources.edge import Edge
from cc.resources.root import Root

__author__ = 'Barak'


def send_admin(path):
    return send_from_directory('admin/ui', path)


def send_to_default():
    return redirect('/admin/index.html')


def normalize_obj(obj):
    if obj.has_key('_id') and not obj.has_key('id'):
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
    resp = make_response(bson.json_util.dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp


def init_app(mongo_url):
    app = Flask(__name__)

    api = flask_restful.Api(app)
    api.representations = {'application/json': output_json}

    app.config['MONGO_URI'] = mongo_url
    mongo.init_app(app)

    app.add_url_rule('/', 'send_to_default', send_to_default)
    app.add_url_rule('/admin/<path:path>', 'send_admin', send_admin)

    api.add_resource(Root, '/api')
    api.add_resource(Monkey, '/api/monkey', '/api/monkey/', '/api/monkey/<string:guid>')
    api.add_resource(LocalRun, '/api/island', '/api/island/')
    api.add_resource(Telemetry, '/api/telemetry', '/api/telemetry/', '/api/telemetry/<string:monkey_guid>')
    api.add_resource(NewConfig, '/api/config/new', '/api/config/new/')
    api.add_resource(MonkeyDownload, '/api/monkey/download', '/api/monkey/download/',
                          '/api/monkey/download/<string:path>')
    api.add_resource(NetMap, '/api/netmap', '/api/netmap/')
    api.add_resource(Edge, '/api/edge', '/api/edge/')

    return app
