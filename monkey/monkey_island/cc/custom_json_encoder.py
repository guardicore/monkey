from bson import ObjectId
from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, ObjectId):
                return obj.__str__()
        except TypeError:
            pass
        return JSONEncoder.default(self, obj)
