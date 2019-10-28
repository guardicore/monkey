from common.cmd.cmd_result import CmdResult

__author__ = 'itay.mizeretz'


class AwsCmdResult(CmdResult):
    """
    Class representing an AWS command result
    """

    def __init__(self, command_info):
        super(AwsCmdResult, self).__init__(
            self.is_successful(command_info, True), command_info['ResponseCode'], command_info['StandardOutputContent'],
            command_info['StandardErrorContent'])
        self.command_info = command_info

    @staticmethod
    def is_successful(command_info, is_timeout=False):
        """
        Determines whether the command was successful. If it timed out and was still in progress, we assume it worked.
        :param command_info:    Command info struct (returned by ssm.get_command_invocation)
        :param is_timeout:      Whether the given command timed out
        :return:                True if successful, False otherwise.
        """
        return (command_info['Status'] == 'Success') or (is_timeout and (command_info['Status'] == 'InProgress'))
