from common.cmd.cmd_result import CmdResult


__author__ = 'itay.mizeretz'


class AwsCmdResult(CmdResult):
    """
    Class representing an AWS command result
    """

    def __init__(self, command_info):
        super(AwsCmdResult, self).__init__(
            self.is_successful(command_info), command_info[u'ResponseCode'], command_info[u'StandardOutputContent'],
            command_info[u'StandardErrorContent'])
        self.command_info = command_info

    @staticmethod
    def is_successful(command_info):
        return command_info[u'Status'] == u'Success'
