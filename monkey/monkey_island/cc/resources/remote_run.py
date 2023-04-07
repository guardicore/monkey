import json
from typing import Sequence

from botocore.exceptions import ClientError, NoCredentialsError
from flask import jsonify, make_response, request
from flask_security import auth_token_required, roles_accepted

from monkey_island.cc.flask_utils import AbstractResource
from monkey_island.cc.services import AWSService
from monkey_island.cc.services.authentication_service import AccountRole
from monkey_island.cc.services.aws import AWSCommandResults

CLIENT_ERROR_FORMAT = (
    "ClientError, error message: '{}'. Probably, the IAM role that has been associated with the "
    "instance doesn't permit SSM calls. "
)
NO_CREDS_ERROR_FORMAT = (
    "NoCredentialsError, error message: '{}'. Probably, no IAM role has been associated with the "
    "instance. "
)


class RemoteRun(AbstractResource):
    # API Spec: POST request is an action, it's not updating/creating any resource.
    # GET makes sense. The resource should be split up since these two use cases don't
    # really go together.
    urls = ["/api/remote-monkey"]

    def __init__(self, aws_service: AWSService):
        self._aws_service = aws_service

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def get(self):
        action = request.args.get("action")
        if action == "list_aws":
            is_aws = self._aws_service.island_is_running_on_aws()
            resp = {"is_aws": is_aws}
            if is_aws:
                try:
                    resp["instances"] = self._aws_service.get_managed_instances()
                except NoCredentialsError as e:
                    # API Spec: HTTP status code should be 401
                    resp["error"] = NO_CREDS_ERROR_FORMAT.format(e)
                    return jsonify(resp)
                except ClientError as e:
                    # API Spec: HTTP status code should not be 200
                    resp["error"] = CLIENT_ERROR_FORMAT.format(e)
                    return jsonify(resp)
            return jsonify(resp)

        return {}

    @auth_token_required
    @roles_accepted(AccountRole.ISLAND_INTERFACE.name)
    def post(self):
        body = json.loads(request.data)
        if body.get("type") == "aws":
            results = self.run_aws_monkeys(body)
            # API Spec: POST should return identifier or updated/newly created resource, not some
            # kind of data. That's a GET thing.
            return RemoteRun._encode_results(results)

        # default action
        # API Spec: Why is this 500? 500 should be returned in case an exception occurs on the
        # server. 40x makes more sense.
        return make_response({"error": "Invalid action"}, 500)

    def run_aws_monkeys(self, request_body) -> Sequence[AWSCommandResults]:
        instances = request_body.get("instances")
        island_ip = request_body.get("island_ip")

        return self._aws_service.run_agents_on_managed_instances(instances, island_ip)

    @staticmethod
    def _encode_results(results: Sequence[AWSCommandResults]):
        result = list(map(RemoteRun._aws_command_results_to_encodable_dict, results))
        response = {"result": result}

        return jsonify(response)

    @staticmethod
    def _aws_command_results_to_encodable_dict(aws_command_results: AWSCommandResults):
        res_dict = aws_command_results.__dict__
        res_dict["status"] = res_dict["status"].name.lower()
        return res_dict
