import flask_restful
from bson import json_util
from flask import request

from monkey_island.cc.database import mongo
from monkey_island.cc.resources.auth.auth import jwt_required


class MonkeyTest(flask_restful.Resource):
    @jwt_required
    def get(self, **kw):
        find_query = json_util.loads(request.args.get('find_query'))
        return {'results': list(mongo.db.monkey.find(find_query))}
