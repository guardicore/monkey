import json

import flask_restful
from bson import ObjectId
from flask import request

from monkey_island.cc.database import mongo
from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.resources.test.utils.telem_store import TestTelemStore
from monkey_island.cc.services.log import LogService
from monkey_island.cc.services.node import NodeService

__author__ = "itay.mizeretz"


class Log(flask_restful.Resource):
    @jwt_required
    def get(self):
        monkey_id = request.args.get('id')
        exists_monkey_id = request.args.get('exists')
        if monkey_id:
            return LogService.get_log_by_monkey_id(ObjectId(monkey_id))
        else:
            return LogService.log_exists(ObjectId(exists_monkey_id))

    # Used by monkey. can't secure.
    @TestTelemStore.store_test_telem
    def post(self):
        telemetry_json = json.loads(request.data)

        monkey_id = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])['_id']
        # This shouldn't contain any unicode characters. this'll take 2 time less space.
        log_data = str(telemetry_json['log'])
        log_id = LogService.add_log(monkey_id, log_data)

        return mongo.db.log.find_one_or_404({"_id": log_id})
