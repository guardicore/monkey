import json
from flask import request, jsonify, make_response
import flask_restful


class RemoteRun(flask_restful.Resource):
    def run_aws_monkey(self, request_body):
        instance_id = request_body.get('instance_id')
        region = request_body.get('region')
        os = request_body.get('os')  # TODO: consider getting this from instance
        island_ip = request_body.get('island_ip')  # TODO: Consider getting this another way. Not easy to determine target interface

    def post(self):
        body = json.loads(request.data)
        if body.get('type') == 'aws':
            local_run = self.run_aws_monkey(body)
            return jsonify(is_running=local_run[0], error_text=local_run[1])

        # default action
        return make_response({'error': 'Invalid action'}, 500)