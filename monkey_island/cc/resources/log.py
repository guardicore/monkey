import json

import flask_restful
from bson import ObjectId
from flask import request

from cc.database import mongo
from cc.services.log import LogService
from cc.services.node import NodeService

__author__ = "itay.mizeretz"


class Log(flask_restful.Resource):
    def get(self):
        monkey_id = request.args.get('id')
        exists_monkey_id = request.args.get('exists')
        if monkey_id:
            return LogService.get_log_by_monkey_id(ObjectId(monkey_id))
        else:
            return LogService.log_exists(ObjectId(exists_monkey_id))

    def post(self):
        telemetry_json = json.loads(request.data)

        monkey_id = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])['_id']
        log_id = LogService.add_log(monkey_id, telemetry_json['log'])

        return mongo.db.log.find_one_or_404({"_id": log_id})
