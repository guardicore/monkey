__author__ = 'itay.mizeretz'


class Cmd(object):
    """
    Class representing a command
    """

    def __init__(self, cmd_runner, cmd_id):
        self.cmd_runner = cmd_runner
        self.cmd_id = cmd_id
