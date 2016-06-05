from flask import Flask, request, abort, send_from_directory
from flask.ext import restful
from flask.ext.pymongo import PyMongo
from flask import make_response
import bson.json_util
import json
from datetime import datetime
from common import *
import tasks_manager

app = Flask(__name__)
app.config.from_object('dbconfig')
mongo = PyMongo(app)

active_connectors = {}

class Root(restful.Resource):
    def get(self):
        return {
            'status': 'OK',
            'mongo': str(mongo.db),
        }


class Job(restful.Resource):
    def get(self, **kw):
        id = request.args.get('id')
        timestamp = request.args.get('timestamp')
        action = request.args.get('action')

        if action == "log":
            return {"log": get_job_log(id)}

        result = {}

        if (id):
            return mongo.db.job.find_one_or_404({"_id": id})
        else:
            result['timestamp'] = datetime.now().isoformat()

        result['objects'] = [x for x in mongo.db.job.find().sort("creation_time", -1)]
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
        contype = request.args.get('type')

        # if no type given - return list of types
        if not contype:
            conlist = []
            for jobclass in available_jobs:
                if jobclass.connector_type.__name__ not in conlist:
                    conlist.append(jobclass.connector_type.__name__)
            return {"oneOf": conlist}

        con = get_connector_by_name(contype)
        if not con:
            return {}
        properties = mongo.db.connector.find_one({"type": con.__class__.__name__})
        if properties:
            con.load_properties(properties)
        ret = con.get_properties()
        ret["password"] = "" # for better security, don't expose password
        return ret

    def post(self, **kw):
        settings_json = json.loads(request.data)
        contype = settings_json.get("type")

        # preserve password if empty given
        properties = mongo.db.connector.find_one({"type": contype})
        if properties and (not settings_json.has_key("password") or not settings_json["password"]):
            settings_json["password"] = properties.get("password")

        return mongo.db.connector.update({"type": contype},
                                         {"$set": settings_json},
                                         upsert=True)

class JobCreation(restful.Resource):
    def get(self, **kw):
        jobtype = request.args.get('type')
        action = request.args.get('action')
        jobid = request.args.get('id')
        if not (jobtype or jobid):
            res = []
            update_connectors()
            for con in available_jobs:
                if con.connector_type.__name__ in active_connectors:
                    res.append({"title": con.__name__, "$ref": "/jobcreate?type=" + con.__name__})
            return {"oneOf": res}

        job = None
        if not jobid:
            job = get_jobclass_by_name(jobtype)()
        else:
            loaded_job = mongo.db.job.find_one({"_id": bson.ObjectId(jobid)})
            if loaded_job:
                job = get_jobclass_by_name(loaded_job.get("type"))()
                job.load_job_properties(loaded_job.get("properties"))

        if action == "delete":
            if loaded_job.get("execution")["state"] == "pending":
                mongo.db.job.remove({"_id": bson.ObjectId(jobid)})
                return {'status': 'ok'}
            else:
                return {'status': 'bad state'}

        if job and job.connector_type.__name__ in active_connectors.keys():
            properties = {
                "type": {
                    "type": "enum",
                    "enum": [job.__class__.__name__],
                    "options": {"hidden": True}
                }
            }
            if (jobid):
                properties["_id"] = {
                    "type": "enum",
                    "enum": [jobid],
                    "name": "ID",
                }

            job_prop = job.get_job_properties()
            for prop in job_prop:
                properties[prop] = dict({})
                properties[prop]["default"] = job_prop[prop]
                if type(job_prop[prop]) is int:
                    properties[prop]["type"] = "number"
                elif type(job_prop[prop]) is bool:
                    properties[prop]["type"] = "boolean"
                else:
                    properties[prop]["type"] = "string"
                enum = job.get_property_function(prop)
                if enum:
                    properties[prop]["enum"] = list(active_connectors[job.connector_type.__name__].__getattribute__(enum)())

            res = dict({
                "title": "%s Job" % jobtype,
                "type": "object",
                "options": {
                    "disable_collapse": True,
                    "disable_properties": True,
                },
                "properties": properties
            })
            return res

        return {}

    def post(self, **kw):
        settings_json = json.loads(request.data)
        jobtype = settings_json.get("type")
        jobid = settings_json.get("id")
        job = None
        for jobclass in available_jobs:
            if jobclass.__name__ == jobtype:
                job = jobclass()
        if not job:
            return {'status': 'bad type'}

        # params validation
        job.load_job_properties(settings_json)
        parsed_prop = job.get_job_properties()
        if jobid:
            res = mongo.db.job.update({"_id": bson.ObjectId(jobid)},
                                      {"$set": {"properties": parsed_prop}})
            if res and (res["ok"] == 1):
                return {'status': 'ok', 'updated': res["nModified"]}
            else:
                return {'status': 'failed'}

        else:
            execution_state = {"taskid": "",
                               "state" : "pending"}
            new_job = {
                "creation_time": datetime.now(),
                "type": jobtype,
                "properties": parsed_prop,
                "execution": execution_state,
            }
            jobid = mongo.db.job.insert(new_job)
            async = tasks_manager.run_task.delay(jobid)
            execution_state["taskid"] = async.id
            mongo.db.job.update({"_id": jobid},
                                {"$set": {"execution": execution_state}})

            return {'status': 'created'}


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


def get_job_log(jobid):
    res = mongo.db.results.find_one({"jobid": bson.ObjectId(jobid)})
    if res:
        return res["log"]
    return []

def update_connectors():
    for con in available_jobs:
        connector_name = con.connector_type.__name__
        if connector_name not in active_connectors:
            active_connectors[connector_name] = con.connector_type()

        if not active_connectors[connector_name].is_connected():
            refresh_connector_config(mongo, active_connectors[connector_name])
            try:
                app.logger.info("Trying to activate connector: %s" % connector_name)
                active_connectors[connector_name].connect()
            except Exception, e:
                active_connectors.pop(connector_name)
                app.logger.info("Error activating connector: %s, reason: %s" % (connector_name, e))

@app.before_first_request
def init():
    update_connectors()

@app.route('/admin/<path:path>')
def send_admin(path):
    return send_from_directory('admin/ui', path)

DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = restful.Api(app)
api.representations = DEFAULT_REPRESENTATIONS

api.add_resource(Root, '/api')
api.add_resource(Job, '/job')
api.add_resource(Connector, '/connector')
api.add_resource(JobCreation, '/jobcreate')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, ssl_context=('server.crt', 'server.key'))
