import time

from common.cloud.aws_service import AwsService
from common.cmd.aws_cmd_result import AwsCmdResult

__author__ = 'itay.mizeretz'


class AwsCmdRunner(object):
    """
    Class for running a command on a remote AWS machine
    """

    def __init__(self, instance_id, region, is_powershell=False):
        self.instance_id = instance_id
        self.region = region
        self.is_powershell = is_powershell
        self.ssm = AwsService.get_client('ssm', region)

    def run_command(self, command, timeout):
        command_id = self._send_command(command)
        init_time = time.time()
        curr_time = init_time
        command_info = None
        while curr_time - init_time < timeout:
            command_info = self.ssm.get_command_invocation(CommandId=command_id, InstanceId=self.instance_id)
            if AwsCmdResult.is_successful(command_info):
                break
            else:
                time.sleep(0.5)
                curr_time = time.time()

        return AwsCmdResult(command_info)

    def _send_command(self, command):
        doc_name = "AWS-RunPowerShellScript" if self.is_powershell else "AWS-RunShellScript"
        command_res = self.ssm.send_command(DocumentName=doc_name, Parameters={'commands': [command]},
                                            InstanceIds=[self.instance_id])
        return command_res['Command']['CommandId']
