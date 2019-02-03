from abc import abstractmethod

__author__ = 'itay.mizeretz'


class CmdRunner(object):
    """
    Interface for running a command on a remote machine
    """

    # Default command timeout in seconds
    DEFAULT_TIMEOUT = 5

    @abstractmethod
    def run_command(self, command, timeout=DEFAULT_TIMEOUT):
        """
        Runs the given command on the remote machine
        :param command: The command to run
        :param timeout: Timeout in seconds for command.
        :return: Command result
        """
        raise NotImplementedError()
