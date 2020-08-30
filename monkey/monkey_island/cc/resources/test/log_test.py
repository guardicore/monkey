import flask_restful
from bson import json_util
from flask import request

from monkey_island.cc.database import database, mongo
from monkey_island.cc.resources.auth.auth import jwt_required


class LogTest(flask_restful.Resource):
    @jwt_required
    def get(self):
        find_query = json_util.loads(request.args.get('find_query'))
        log = mongo.db.log.find_one(find_query)
        if not log:
            return {'results': None}
        log_file = database.gridfs.get(log['file_id'])
        return {'results': log_file.read().decode()}
