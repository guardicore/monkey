from datetime import datetime

import bson
from flask import Flask, send_from_directory, redirect, make_response
import flask_restful

from cc.database import mongo
from cc.resources.monkey import Monkey
from cc.resources.local_run import LocalRun
from cc.resources.telemetry import Telemetry
from cc.resources.monkey_configuration import MonkeyConfiguration
from cc.resources.monkey_download import MonkeyDownload
from cc.resources.netmap import NetMap
from cc.resources.edge import Edge
from cc.resources.root import Root

__author__ = 'Barak'


def serve_static_file(path):
    print 'requested', path
    return send_from_directory('ui/dist', path)


def serve_home():
    return serve_static_file('index.html')


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


def init_app(mongo_url):
    app = Flask(__name__)

    api = flask_restful.Api(app)

    app.config['MONGO_URI'] = mongo_url
    mongo.init_app(app)

    app.add_url_rule('/', 'serve_home', serve_home)
    app.add_url_rule('/<path:path>', 'serve_static_file', serve_static_file)

    api.add_resource(Root, '/api')
    api.add_resource(Monkey, '/api/monkey', '/api/monkey/', '/api/monkey/<string:guid>')
    api.add_resource(LocalRun, '/api/island', '/api/island/')
    api.add_resource(Telemetry, '/api/telemetry', '/api/telemetry/', '/api/telemetry/<string:monkey_guid>')
    api.add_resource(MonkeyConfiguration, '/api/configuration', '/api/configuration/')
    api.add_resource(MonkeyDownload, '/api/monkey/download', '/api/monkey/download/',
                          '/api/monkey/download/<string:path>')
    api.add_resource(NetMap, '/api/netmap', '/api/netmap/')
    api.add_resource(Edge, '/api/edge', '/api/edge/')

    return app
