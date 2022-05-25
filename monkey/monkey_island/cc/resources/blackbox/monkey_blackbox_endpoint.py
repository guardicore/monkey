from bson import json_util
from flask import request

from monkey_island.cc.database import mongo
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required


class MonkeyBlackboxEndpoint(AbstractResource):
    urls = ["/api/test/monkey"]

    @jwt_required
    def get(self, **kw):
        find_query = json_util.loads(request.args.get("find_query"))
        return {"results": list(mongo.db.monkey.find(find_query))}
