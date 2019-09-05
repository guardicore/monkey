import json

import flask_restful
from flask import request

from monkey_island.cc.auth import jwt_required
from monkey_island.cc.database import mongo


class MonkeyTest(flask_restful.Resource):
    @jwt_required()
    def get(self, **kw):
        find_query = json.loads(request.args.get('find_query'))
        return {'results': list(mongo.db.monkey.find(find_query))}
