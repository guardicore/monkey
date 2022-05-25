from bson import json_util
from flask import request

from monkey_island.cc.database import database, mongo
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required


class LogBlackboxEndpoint(AbstractResource):
    urls = ["/api/test/log"]

    @jwt_required
    def get(self):
        find_query = json_util.loads(request.args.get("find_query"))
        log = mongo.db.log.find_one(find_query)
        if not log:
            return {"results": None}
        log_file = database.gridfs.get(log["file_id"])
        return {"results": log_file.read().decode()}
