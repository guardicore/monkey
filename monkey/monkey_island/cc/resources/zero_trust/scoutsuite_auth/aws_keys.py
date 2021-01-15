import flask_restful

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.zero_trust.scoutsuite.scoutsuite_auth_service import get_aws_keys


class AWSKeys(flask_restful.Resource):

    @jwt_required
    def get(self):
        return get_aws_keys()
