import json

import flask_restful
from botocore.exceptions import ClientError, NoCredentialsError
from flask import jsonify, make_response, request

from common.cloud.aws.aws_service import AwsService
from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services.remote_run_aws import RemoteRunAwsService

CLIENT_ERROR_FORMAT = "ClientError, error message: '{}'. Probably, the IAM role that has been associated with the " \
                      "instance doesn't permit SSM calls. "
NO_CREDS_ERROR_FORMAT = "NoCredentialsError, error message: '{}'. Probably, no IAM role has been associated with the " \
                        "instance. "


class RemoteRun(flask_restful.Resource):
    def __init__(self):
        super(RemoteRun, self).__init__()
        RemoteRunAwsService.init()

    def run_aws_monkeys(self, request_body):
        instances = request_body.get('instances')
        island_ip = request_body.get('island_ip')
        return RemoteRunAwsService.run_aws_monkeys(instances, island_ip)

    @jwt_required
    def get(self):
        action = request.args.get('action')
        if action == 'list_aws':
            is_aws = RemoteRunAwsService.is_running_on_aws()
            resp = {'is_aws': is_aws}
            if is_aws:
                try:
                    resp['instances'] = AwsService.get_instances()
                except NoCredentialsError as e:
                    resp['error'] = NO_CREDS_ERROR_FORMAT.format(e)
                    return jsonify(resp)
                except ClientError as e:
                    resp['error'] = CLIENT_ERROR_FORMAT.format(e)
                    return jsonify(resp)
            return jsonify(resp)

        return {}

    @jwt_required
    def post(self):
        body = json.loads(request.data)
        resp = {}
        if body.get('type') == 'aws':
            RemoteRunAwsService.update_aws_region_authless()
            result = self.run_aws_monkeys(body)
            resp['result'] = result
            return jsonify(resp)

        # default action
        return make_response({'error': 'Invalid action'}, 500)
