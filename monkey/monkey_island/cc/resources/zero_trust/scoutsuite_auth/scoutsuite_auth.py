import json

import flask_restful
from flask import request

from common.cloud.scoutsuite_consts import CloudProviders
from common.utils.exceptions import InvalidAWSKeys
from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.zero_trust.scoutsuite.scoutsuite_auth_service import (is_cloud_authentication_setup,
                                                                                     set_aws_keys)


class ScoutSuiteAuth(flask_restful.Resource):

    @jwt_required
    def get(self, provider: CloudProviders):
        if provider == CloudProviders.AWS.value:
            is_setup, message = is_cloud_authentication_setup(provider)
            return {'is_setup': is_setup, 'message': message}
        else:
            return {'is_setup': False, 'message': ''}

    @jwt_required
    def post(self, provider: CloudProviders):
        key_info = json.loads(request.data)
        error_msg = ''
        if provider == CloudProviders.AWS.value:
            try:
                set_aws_keys(access_key_id=key_info['accessKeyId'],
                             secret_access_key=key_info['secretAccessKey'],
                             session_token=key_info['sessionToken'])
            except InvalidAWSKeys as e:
                error_msg = str(e)
        return {'error_msg': error_msg}
