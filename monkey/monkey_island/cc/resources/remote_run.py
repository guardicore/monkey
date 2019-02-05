import json
from flask import request, jsonify, make_response
import flask_restful

from cc.auth import jwt_required
from cc.services.config import ConfigService
from common.cloud.aws_instance import AwsInstance
from common.cloud.aws_service import AwsService
from common.cmd.aws_cmd_runner import AwsCmdRunner
from common.cmd.cmd_runner import CmdRunner


class RemoteRun(flask_restful.Resource):
    def __init__(self):
        super(RemoteRun, self).__init__()
        self.aws_instance = AwsInstance()

    def run_aws_monkeys(self, request_body):
        self.init_aws_auth_params()
        instances = request_body.get('instances')
        island_ip = request_body.get('island_ip')
        instances_bitness = self.get_bitness(instances)
        return self.run_multiple_commands(
            instances,
            lambda instance: self.run_aws_monkey_cmd_async(instance['instance_id'],
                                                           instance['os'], island_ip, instances_bitness[instance['instance_id']]),
            lambda _, result: result.is_success)

    def run_multiple_commands(self, instances, inst_to_cmd, inst_n_cmd_res_to_res):
        command_instance_dict = {}

        for instance in instances:
            command = inst_to_cmd(instance)
            command_instance_dict[command] = instance

        instance_results = {}
        results = CmdRunner.wait_commands(command_instance_dict.keys())
        for command, result in results:
            instance = command_instance_dict[command]
            instance_results[instance['instance_id']] = inst_n_cmd_res_to_res(instance, result)

        return instance_results

    def get_bitness(self, instances):
        return self.run_multiple_commands(
            instances,
            lambda instance: RemoteRun.run_aws_bitness_cmd_async(instance['instance_id'], instance['os']),
            lambda instance, result: self.get_bitness_by_result('linux' == instance['os'], result))

    def get_bitness_by_result(self, is_linux, result):
        if not result.is_success:
            return None
        elif is_linux:
            return result.stdout.find('i686') == -1  # i686 means 32bit
        else:
            return result.stdout.lower().find('programfiles(x86)') != -1  # if not found it means 32bit

    @staticmethod
    def run_aws_bitness_cmd_async(instance_id, os):
        """
        Runs an AWS command to check bitness
        :param instance_id: Instance ID of target
        :param os:          OS of target ('linux' or 'windows')
        :return:            Tuple of CmdRunner and command id
        """
        is_linux = ('linux' == os)
        cmd = AwsCmdRunner(instance_id, None, is_linux)
        cmd_text = 'uname -m' if is_linux else 'Get-ChildItem Env:'
        return cmd, cmd.run_command_async(cmd_text)

    def run_aws_monkey_cmd_async(self, instance_id, os, island_ip, is_64bit):
        """
        Runs a monkey remotely using AWS
        :param instance_id: Instance ID of target
        :param os:          OS of target ('linux' or 'windows')
        :param island_ip:   IP of the island which the instance will try to connect to
        :param is_64bit:    Whether the instance is 64bit
        :return:            Tuple of CmdRunner and command id
        """
        is_linux = ('linux' == os)
        cmd = AwsCmdRunner(instance_id, None, is_linux)
        cmd_text = self._get_run_monkey_cmd_line(is_linux, is_64bit, island_ip)
        return cmd, cmd.run_command_async(cmd_text)

    def _get_run_monkey_cmd_linux_line(self, bit_text, island_ip):
        return r'wget --no-check-certificate https://' + island_ip + r':5000/api/monkey/download/monkey-linux-' + \
               bit_text + r'; chmod +x monkey-linux-' + bit_text + r'; ./monkey-linux-' + bit_text + r' m0nk3y -s ' + \
               island_ip + r':5000'

    def _get_run_monkey_cmd_windows_line(self, bit_text, island_ip):
        return r"[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {" \
               r"$true}; (New-Object System.Net.WebClient).DownloadFile('https://" + island_ip + \
               r":5000/api/monkey/download/monkey-windows-" + bit_text + r".exe','.\\monkey.exe'); " \
               r";Start-Process -FilePath '.\\monkey.exe' -ArgumentList 'm0nk3y -s " + island_ip + r":5000'; "

    def _get_run_monkey_cmd_line(self, is_linux, is_64bit, island_ip):
        bit_text = '64' if is_64bit else '32'
        return self._get_run_monkey_cmd_linux_line(bit_text, island_ip) if is_linux \
            else self._get_run_monkey_cmd_windows_line(bit_text, island_ip)

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
