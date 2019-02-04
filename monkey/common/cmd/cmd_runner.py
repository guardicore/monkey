from abc import abstractmethod

__author__ = 'itay.mizeretz'


class CmdRunner(object):
    """
    Interface for running a command on a remote machine
    """

    # Default command timeout in seconds
    DEFAULT_TIMEOUT = 5

    def __init__(self, is_linux):
        self.is_linux = is_linux

    @abstractmethod
    def run_command(self, command, timeout=DEFAULT_TIMEOUT):
        """
        Runs the given command on the remote machine
        :param command: The command to run
        :param timeout: Timeout in seconds for command.
        :return: Command result
        """
        raise NotImplementedError()

    def is_64bit(self):
        """
        Runs a command to determine whether OS is 32 or 64 bit.
        :return: True if 64bit, False if 32bit, None if failed.
        """
        if self.is_linux:
            cmd_result = self.run_command('uname -m')
            if not cmd_result.is_success:
                return None
            return cmd_result.stdout.find('i686') == -1  # i686 means 32bit
        else:
            cmd_result = self.run_command('Get-ChildItem Env:')
            if not cmd_result.is_success:
                return None
            return cmd_result.stdout.lower().find('programfiles(x86)') != -1  # if not found it means 32bit
