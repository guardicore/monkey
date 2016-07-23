import os
from flask import Flask, request, abort, send_from_directory
from flask.ext import restful
from flask.ext.pymongo import PyMongo
from flask import make_response
import bson.json_util
import json
from datetime import datetime, timedelta
import dateutil.parser

MONKEY_DOWNLOADS = [
    {
        'type': 'linux',
        'machine': 'x86_64',
        'filename': 'monkey-linux-64',
    },
    {
        'type': 'linux',
        'machine': 'i686',
        'filename': 'monkey-linux-32',
    },
    {
        'type': 'linux',
        'filename': 'monkey-linux-32',
    },
    {
        'type': 'windows',
        'machine': 'x86',
        'filename': 'monkey-windows-32.exe',
    },
    {
        'type': 'windows',
        'machine': 'amd64',
        'filename': 'monkey-windows-64.exe',
    },
    {
        'type': 'windows',
        'filename': 'monkey-windows-32.exe',
    },
]

MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/monkeyisland"

app = Flask(__name__)
app.config['MONGO_URI'] = MONGO_URL
mongo = PyMongo(app)


class Monkey(restful.Resource):
    def get(self, guid=None, **kw):
        update_dead_monkeys()  # refresh monkeys status
        if not guid:
            guid = request.args.get('guid')
        timestamp = request.args.get('timestamp')

        if guid:
            return mongo.db.monkey.find_one_or_404({"guid": guid})
        else:
            result = {'timestamp': datetime.now().isoformat()}
            find_filter = {}
            if timestamp is not None:
                find_filter['modifytime'] = {'$gt': dateutil.parser.parse(timestamp)}
            result['objects'] = [x for x in mongo.db.monkey.find(find_filter)]
            return result

    def patch(self, guid):
        monkey_json = json.loads(request.data)
        update = {"$set": {'modifytime': datetime.now()}}

        if monkey_json.has_key('keepalive'):
            update['$set']['keepalive'] = dateutil.parser.parse(monkey_json['keepalive'])
        else:
            update['$set']['keepalive'] = datetime.now()
        if monkey_json.has_key('config'):
            update['$set']['config'] = monkey_json['config']
        if monkey_json.has_key('tunnel'):
            update['$set']['tunnel'] = monkey_json['tunnel']

        return mongo.db.monkey.update({"guid": guid}, update, upsert=False)

    def post(self, **kw):
        monkey_json = json.loads(request.data)
        if monkey_json.has_key('keepalive'):
            monkey_json['keepalive'] = dateutil.parser.parse(monkey_json['keepalive'])
        else:
            monkey_json['keepalive'] = datetime.now()

        monkey_json['modifytime'] = datetime.now()

        # if new monkey telem, change config according to "new monkeys" config.
        db_monkey = mongo.db.monkey.find_one({"guid": monkey_json["guid"]})
        if not db_monkey:
            new_config = mongo.db.config.find_one({'name': 'newconfig'}) or {}
            monkey_json['config'] = monkey_json.get('config', {})
            monkey_json['config'].update(new_config)
        else:
            db_config = db_monkey.get('config', {})
            if db_config.has_key('current_server'):
                del db_config['current_server']
            monkey_json.get('config', {}).update(db_config)

        # try to find new monkey parent
        parent = monkey_json.get('parent')
        parent_to_add = (monkey_json.get('guid'), None)  # default values in case of manual run
        if parent and parent != monkey_json.get('guid'):  # current parent is known
            exploit_telem = [x for x in
                             mongo.db.telemetry.find({'telem_type': {'$eq': 'exploit'}, 'data.result': {'$eq': True},
                                                      'data.machine.ip_addr': {'$in': monkey_json['ip_addresses']},
                                                      'monkey_guid': {'$eq': parent}})]
            if 1 == len(exploit_telem):
                parent_to_add = (exploit_telem[0].get('monkey_guid'), exploit_telem[0].get('data').get('exploiter'))
            else:
                parent_to_add = (parent, None)
        elif (not parent or parent == monkey_json.get('guid')) and monkey_json.has_key('ip_addresses'):
            exploit_telem = [x for x in
                             mongo.db.telemetry.find({'telem_type': {'$eq': 'exploit'}, 'data.result': {'$eq': True},
                                                      'data.machine.ip_addr': {'$in': monkey_json['ip_addresses']}})]

            if 1 == len(exploit_telem):
                parent_to_add = (exploit_telem[0].get('monkey_guid'), exploit_telem[0].get('data').get('exploiter'))

        if not db_monkey:
            monkey_json['parent'] = [parent_to_add]
        else:
            monkey_json['parent'] = db_monkey.get('parent') + [parent_to_add]

        return mongo.db.monkey.update({"guid": monkey_json["guid"]},
                                      {"$set": monkey_json},
                                      upsert=True)


class Telemetry(restful.Resource):
    def get(self, **kw):
        monkey_guid = request.args.get('monkey_guid')
        telem_type = request.args.get('telem_type')
        timestamp = request.args.get('timestamp')
        if "null" == timestamp:  # special case to avoid ugly JS code...
            timestamp = None

        result = {'timestamp': datetime.now().isoformat()}
        find_filter = {}

        if monkey_guid:
            find_filter["monkey_guid"] = {'$eq': monkey_guid}
        if telem_type:
            find_filter["telem_type"] = {'$eq': telem_type}
        if timestamp:
            find_filter['timestamp'] = {'$gt': dateutil.parser.parse(timestamp)}

        result['objects'] = [x for x in mongo.db.telemetry.find(find_filter)]
        return result

    def post(self):
        telemetry_json = json.loads(request.data)
        telemetry_json['timestamp'] = datetime.now()

        telem_id = mongo.db.telemetry.insert(telemetry_json)

        # update exploited monkeys parent
        try:
            if telemetry_json.get('telem_type') == 'tunnel':
                if telemetry_json['data']:
                    host = telemetry_json['data'].split(":")[-2].replace("//", "")
                    tunnel_host = mongo.db.monkey.find_one({"ip_addresses": host})
                    mongo.db.monkey.update({"guid": telemetry_json['monkey_guid']},
                                           {'$set': {'tunnel_guid': tunnel_host.get('guid')}},
                                           upsert=False)
                else:
                    mongo.db.monkey.update({"guid": telemetry_json['monkey_guid']},
                                           {'$unset': {'tunnel_guid': ''}},
                                           upsert=False)
            elif telemetry_json.get('telem_type') == 'state':
                if telemetry_json['data']['done']:
                    mongo.db.monkey.update({"guid": telemetry_json['monkey_guid']},
                                           {'$set': {'dead': True}},
                                           upsert=False)
                else:
                    mongo.db.monkey.update({"guid": telemetry_json['monkey_guid']},
                                           {'$set': {'dead': False}},
                                           upsert=False)
        except:
            pass

        return mongo.db.telemetry.find_one_or_404({"_id": telem_id})


class NewConfig(restful.Resource):
    def get(self):
        config = mongo.db.config.find_one({'name': 'newconfig'}) or {}
        if config.has_key('name'):
            del config['name']
        return config

    def post(self):
        config_json = json.loads(request.data)
        return mongo.db.config.update({'name': 'newconfig'}, {"$set": config_json}, upsert=True)


class MonkeyDownload(restful.Resource):
    def get(self, path):
        return send_from_directory('binaries', path)

    def post(self):
        host_json = json.loads(request.data)
        host_os = host_json.get('os')
        if host_os:
            result = None
            for download in MONKEY_DOWNLOADS:
                if host_os.get('type') == download.get('type') and \
                                host_os.get('machine') == download.get('machine'):
                    result = download
                    break

            if result:
                real_path = os.path.join('binaries', result['filename'])
                if os.path.isfile(real_path):
                    result['size'] = os.path.getsize(real_path)
                    return result

        return {}


class Root(restful.Resource):
    def get(self):
        return {
            'status': 'OK',
            'mongo': str(mongo.db),
        }


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


def update_dead_monkeys():
    mongo.db.monkey.update(
        {'keepalive': {'$lte': datetime.now() - timedelta(minutes=10)}, 'dead': {'$ne': True}},
        {'$set': {'dead': True, 'modifytime': datetime.now()}}, upsert=False)


@app.route('/admin/<path:path>')
def send_admin(path):
    return send_from_directory('admin/ui', path)


DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = restful.Api(app)
api.representations = DEFAULT_REPRESENTATIONS

api.add_resource(Root, '/api')
api.add_resource(Monkey, '/api/monkey', '/api/monkey/', '/api/monkey/<string:guid>')
api.add_resource(Telemetry, '/api/telemetry', '/api/telemetry/', '/api/telemetry/<string:monkey_guid>')
api.add_resource(NewConfig, '/api/config/new')
api.add_resource(MonkeyDownload, '/api/monkey/download', '/api/monkey/download/', '/api/monkey/download/<string:path>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, ssl_context=('server.crt', 'server.key'))
