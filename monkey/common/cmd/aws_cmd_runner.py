import time
import logging
import json

from common.cloud.aws_service import AwsService
from common.cmd.aws_cmd_result import AwsCmdResult
from common.cmd.cmd_result import CmdResult
from common.cmd.cmd_runner import CmdRunner

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

    def run_command(self, command, timeout=CmdRunner.DEFAULT_TIMEOUT):
        # TODO: document
        command_id = self._send_command(command)
        init_time = time.time()
        curr_time = init_time
        command_info = None

        try:
            while curr_time - init_time < timeout:
                command_info = self.ssm.get_command_invocation(CommandId=command_id, InstanceId=self.instance_id)
                if AwsCmdResult.is_successful(command_info):
                    break
                else:
                    time.sleep(0.5)
                    curr_time = time.time()

            cmd_res = AwsCmdResult(command_info)

            if not cmd_res.is_success:
                logger.error('Failed running AWS command: `%s`. status code: %s', command, str(cmd_res.status_code))

            return cmd_res
        except Exception:
            logger.exception('Exception while running AWS command: `%s`', command)
            return CmdResult(False)

    def _send_command(self, command):
        doc_name = "AWS-RunShellScript" if self.is_linux else "AWS-RunPowerShellScript"
        command_res = self.ssm.send_command(DocumentName=doc_name, Parameters={'commands': [command]},
                                            InstanceIds=[self.instance_id])
        return command_res['Command']['CommandId']
