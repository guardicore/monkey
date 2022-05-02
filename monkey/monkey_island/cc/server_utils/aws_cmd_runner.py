import logging
import time

from common.cmd.cmd_runner import CmdRunner
from common.cmd.cmd_status import CmdStatus
from monkey_island.cc.server_utils.aws_cmd_result import AwsCmdResult
from monkey_island.cc.services import aws_service

logger = logging.getLogger(__name__)


class AwsCmdRunner(CmdRunner):
    """
    Class for running commands on a remote AWS machine
    """

    def __init__(self, is_linux, instance_id, region=None):
        super(AwsCmdRunner, self).__init__(is_linux)
        self.instance_id = instance_id
        self.region = region
        self.ssm = aws_service.get_client("ssm", region)

    def query_command(self, command_id):
        time.sleep(2)
        return self.ssm.get_command_invocation(CommandId=command_id, InstanceId=self.instance_id)

    def get_command_result(self, command_info):
        return AwsCmdResult(command_info)

    def get_command_status(self, command_info):
        if command_info["Status"] == "InProgress":
            return CmdStatus.IN_PROGRESS
        elif command_info["Status"] == "Success":
            return CmdStatus.SUCCESS
        else:
            return CmdStatus.FAILURE

    def run_command_async(self, command_line):
        doc_name = "AWS-RunShellScript" if self.is_linux else "AWS-RunPowerShellScript"
        command_res = self.ssm.send_command(
            DocumentName=doc_name,
            Parameters={"commands": [command_line]},
            InstanceIds=[self.instance_id],
        )
        return command_res["Command"]["CommandId"]
