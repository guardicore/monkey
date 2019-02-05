import time
import logging

from common.cloud.aws_service import AwsService
from common.cmd.aws_cmd_result import AwsCmdResult
from common.cmd.cmd_result import CmdResult
from common.cmd.cmd_runner import CmdRunner
from common.cmd.cmd_status import CmdStatus

__author__ = 'itay.mizeretz'

logger = logging.getLogger(__name__)


class AwsCmdRunner(CmdRunner):
    """
    Class for running a command on a remote AWS machine
    """

    def __init__(self, instance_id, region, is_linux):
        super(AwsCmdRunner, self).__init__(is_linux)
        self.instance_id = instance_id
        self.region = region
        self.ssm = AwsService.get_client('ssm', region)

    def query_command(self, command_id):
        return self.ssm.get_command_invocation(CommandId=command_id, InstanceId=self.instance_id)

    def get_command_result(self, command_info):
        return AwsCmdResult(command_info)

    def get_command_status(self, command_info):
        if command_info[u'Status'] == u'InProgress':
            return CmdStatus.IN_PROGRESS
        elif command_info[u'Status'] == u'Success':
            return CmdStatus.SUCCESS
        else:
            return CmdStatus.FAILURE

    def run_command_async(self, command):
        doc_name = "AWS-RunShellScript" if self.is_linux else "AWS-RunPowerShellScript"
        command_res = self.ssm.send_command(DocumentName=doc_name, Parameters={'commands': [command]},
                                            InstanceIds=[self.instance_id])
        return command_res['Command']['CommandId']
