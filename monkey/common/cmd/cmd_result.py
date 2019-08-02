__author__ = 'itay.mizeretz'


class CmdResult(object):
    """
    Class representing a command result
    """

    def __init__(self, is_success, status_code=None, stdout=None, stderr=None):
        self.is_success = is_success
        self.status_code = status_code
        self.stdout = stdout
        self.stderr = stderr
