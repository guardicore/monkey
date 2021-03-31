from bson import ObjectId, json_util
from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, ObjectId):
                return json_util.dumps(obj)
        except TypeError:
            pass
        return JSONEncoder.default(self, obj)
