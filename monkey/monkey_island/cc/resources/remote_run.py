import json
from flask import request, jsonify, make_response
import flask_restful

from cc.auth import jwt_required
from cc.services.remote_run_aws import RemoteRunAwsService
from common.cloud.aws_service import AwsService


class RemoteRun(flask_restful.Resource):
    def __init__(self):
        super(RemoteRun, self).__init__()
        RemoteRunAwsService.init()

    def run_aws_monkeys(self, request_body):
        instances = request_body.get('instances')
        island_ip = request_body.get('island_ip')
        return RemoteRunAwsService.run_aws_monkeys(instances, island_ip)

    @jwt_required()
    def get(self):
        action = request.args.get('action')
        if action == 'list_aws':
            is_aws = RemoteRunAwsService.is_running_on_aws()
            resp = {'is_aws': is_aws}
            if is_aws:
                is_auth = RemoteRunAwsService.update_aws_auth_params()
                resp['auth'] = is_auth
                if is_auth:
                    resp['instances'] = AwsService.get_instances()
            return jsonify(resp)

        return {}

    @jwt_required()
    def post(self):
        body = json.loads(request.data)
        resp = {}
        if body.get('type') == 'aws':
            is_auth = RemoteRunAwsService.update_aws_auth_params()
            resp['auth'] = is_auth
            if is_auth:
                result = self.run_aws_monkeys(body)
                resp['result'] = result
            return jsonify(resp)

        # default action
        return make_response({'error': 'Invalid action'}, 500)
