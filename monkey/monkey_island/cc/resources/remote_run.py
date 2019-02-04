import json
from flask import request, jsonify, make_response
import flask_restful

from cc.auth import jwt_required
from cc.services.config import ConfigService
from common.cloud.aws_instance import AwsInstance
from common.cloud.aws_service import AwsService
from common.cmd.aws_cmd_runner import AwsCmdRunner


class RemoteRun(flask_restful.Resource):
    def __init__(self):
        super(RemoteRun, self).__init__()
        self.aws_instance = AwsInstance()

    def run_aws_monkeys(self, request_body):
        self.init_aws_auth_params()
        instances = request_body.get('instances')
        island_ip = request_body.get('island_ip')

        results = {}

        for instance in instances:
            is_success = self.run_aws_monkey_cmd(instance['instance_id'], instance['os'], island_ip)
            results[instance['instance_id']] = is_success

        return results

    def run_aws_monkey_cmd(self, instance_id, os, island_ip):
        """
        Runs a monkey remotely using AWS
        :param instance_id: Instance ID of target
        :param os:          OS of target ('linux' or 'windows')
        :param island_ip:   IP of the island which the instance will try to connect to
        :return:            True if successfully ran monkey, False otherwise.
        """
        is_linux = ('linux' == os)
        cmd = AwsCmdRunner(instance_id, None, is_linux)
        is_64bit = cmd.is_64bit()
        cmd_text = self._get_run_monkey_cmd(is_linux, is_64bit, island_ip)
        return cmd.run_command(cmd_text).is_success

    def _get_run_monkey_cmd_linux(self, bit_text, island_ip):
        return r'wget --no-check-certificate https://' + island_ip + r':5000/api/monkey/download/monkey-linux-' + \
               bit_text + r'; chmod +x monkey-linux-' + bit_text + r'; ./monkey-linux-' + bit_text + r' m0nk3y -s ' + \
               island_ip + r':5000'
        """
        return r'curl -O -k https://' + island_ip + r':5000/api/monkey/download/monkey-linux-' + bit_text + \
               r'; chmod +x monkey-linux-' + bit_text + \
               r'; ./monkey-linux-' + bit_text + r' m0nk3y -s ' + \
               island_ip + r':5000'
               """

    def _get_run_monkey_cmd_windows(self, bit_text, island_ip):
        return r"[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {" \
               r"$true}; (New-Object System.Net.WebClient).DownloadFile('https://" + island_ip + \
               r":5000/api/monkey/download/monkey-windows-" + bit_text + r".exe','.\\monkey.exe'); " \
               r";Start-Process -FilePath '.\\monkey.exe' -ArgumentList 'm0nk3y -s " + island_ip + r":5000'; "

    def _get_run_monkey_cmd(self, is_linux, is_64bit, island_ip):
        bit_text = '64' if is_64bit else '32'
        return self._get_run_monkey_cmd_linux(bit_text, island_ip) if is_linux \
            else self._get_run_monkey_cmd_windows(bit_text, island_ip)

    def init_aws_auth_params(self):
        access_key_id = ConfigService.get_config_value(['cnc', 'aws_config', 'aws_access_key_id'], False, True)
        secret_access_key = ConfigService.get_config_value(['cnc', 'aws_config', 'aws_secret_access_key'], False, True)
        AwsService.set_auth_params(access_key_id, secret_access_key)
        AwsService.set_region(self.aws_instance.region)

    @jwt_required()
    def get(self):
        action = request.args.get('action')
        if action == 'list_aws':
            is_aws = self.aws_instance.is_aws_instance()
            resp = {'is_aws': is_aws}
            if is_aws:
                resp['instances'] = AwsService.get_instances()
            self.init_aws_auth_params()
            return jsonify(resp)

        return {}

    @jwt_required()
    def post(self):
        body = json.loads(request.data)
        if body.get('type') == 'aws':
            result = self.run_aws_monkeys(body)
            return jsonify({'result': result})

        # default action
        return make_response({'error': 'Invalid action'}, 500)
