from typing import List

import flask_restful


# The purpose of this class is to decouple resources from flask
class AbstractResource(flask_restful.Resource):
    urls: List[str] = []
