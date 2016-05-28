import os
from flask import Flask, request, abort, send_from_directory
from flask.ext import restful
from flask.ext.pymongo import PyMongo
from flask import make_response
import bson.json_util
import json
from datetime import datetime
import dateutil.parser
from connectors.vcenter import VCenterConnector

MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/monkeybusiness"

app = Flask(__name__)
app.config['MONGO_URI'] = MONGO_URL
mongo = PyMongo(app)

class Root(restful.Resource):
    def get(self):
        return {
            'status': 'OK',
            'mongo': str(mongo.db),
        }


class Job(restful.Resource):
    def get(self, **kw):
        id = kw.get('id')
        timestamp = request.args.get('timestamp')

        if (id):
            return mongo.db.job.find_one_or_404({"id": id})
        else:
            result = {'timestamp': datetime.now().isoformat()}

        find_filter = {}
        if None != timestamp:
            find_filter['modifytime'] = {'$gt': dateutil.parser.parse(timestamp)}
        result['objects'] = [x for x in mongo.db.job.find(find_filter)]
        return result

    def post(self, **kw):
        job_json = json.loads(request.data)

        job_json["modifytime"] = datetime.now()

        if job_json.has_key('pk'):
            job = mongo.db.job.find_one_or_404({"pk": job_json["pk"]})

            if "pending" != job.get("status"):
                res = {"status": "cannot change job at this state", "res" : 0}
                return res
            if "delete" == job_json["action"]:
                return mongo.db.job.delete_one({"pk": job_json["pk"]})

        # update job
        job_json["status"] = "pending"
        return mongo.db.job.update({"pk": job_json["pk"]},
                                   {"$set": job_json},
                                   upsert=True)

class Connector(restful.Resource):
    def get(self, **kw):
        type = request.args.get('type')
        if (type == 'vcenter'):
            vcenter = VCenterConnector()
            properties = mongo.db.connector.find_one({"type": 'vcenter'})
            if properties:
                vcenter.load_properties(properties)
            ret = vcenter.get_properties()
            ret["password"] = "" # for better security, don't expose password
            return ret
        return {}

    def post(self, **kw):
        settings_json = json.loads(request.data)
        if (settings_json.get("type") == 'vcenter'):

            # preserve password
            properties = mongo.db.connector.find_one({"type": 'vcenter'})
            if properties and (not settings_json.has_key("password") or not settings_json["password"]):
                settings_json["password"] = properties.get("password")

            return mongo.db.connector.update({"type": 'vcenter'},
                                               {"$set": settings_json},
                                               upsert=True)


def normalize_obj(obj):
    if obj.has_key('_id') and not obj.has_key('id'):
        obj['id'] = obj['_id']
        del obj['_id']

    for key,value in obj.items():
        if type(value) is bson.objectid.ObjectId:
            obj[key] = str(value)
        if type(value) is datetime:
            obj[key] = str(value)
        if type(value) is dict:
            obj[key] = normalize_obj(value)
        if type(value) is list:
            for i in range(0,len(value)):
                if type(value[i]) is dict:
                    value[i] = normalize_obj(value[i])
    return obj


def output_json(obj, code, headers=None):
    obj = normalize_obj(obj)
    resp = make_response(bson.json_util.dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

@app.route('/admin/<path:path>')
def send_admin(path):
    return send_from_directory('admin/ui', path)

DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = restful.Api(app)
api.representations = DEFAULT_REPRESENTATIONS

api.add_resource(Root, '/api')
api.add_resource(Job, '/job')
api.add_resource(Connector, '/connector')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, ssl_context=('server.crt', 'server.key'))
