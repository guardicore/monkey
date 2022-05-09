import json

import flask_restful
from botocore.exceptions import ClientError, NoCredentialsError
from flask import jsonify, make_response, request

from monkey_island.cc.resources.auth.auth import jwt_required
from monkey_island.cc.services import AWSService

CLIENT_ERROR_FORMAT = (
    "ClientError, error message: '{}'. Probably, the IAM role that has been associated with the "
    "instance doesn't permit SSM calls. "
)
NO_CREDS_ERROR_FORMAT = (
    "NoCredentialsError, error message: '{}'. Probably, no IAM role has been associated with the "
    "instance. "
)


class RemoteRun(flask_restful.Resource):
    def __init__(self, aws_service: AWSService):
        self._aws_service = aws_service

    def run_aws_monkeys(self, request_body):
        instances = request_body.get("instances")
        island_ip = request_body.get("island_ip")

        return self._aws_service.run_agents_on_managed_instances(instances, island_ip)

    @jwt_required
    def get(self):
        action = request.args.get("action")
        if action == "list_aws":
            is_aws = self._aws_service.island_is_running_on_aws()
            resp = {"is_aws": is_aws}
            if is_aws:
                try:
                    resp["instances"] = self._aws_service.get_managed_instances()
                except NoCredentialsError as e:
                    resp["error"] = NO_CREDS_ERROR_FORMAT.format(e)
                    return jsonify(resp)
                except ClientError as e:
                    resp["error"] = CLIENT_ERROR_FORMAT.format(e)
                    return jsonify(resp)
            return jsonify(resp)

        return {}

    @jwt_required
    def post(self):
        body = json.loads(request.data)
        resp = {}
        if body.get("type") == "aws":
            result = self.run_aws_monkeys(body)
            resp["result"] = result
            return jsonify(resp)

        # default action
        return make_response({"error": "Invalid action"}, 500)
