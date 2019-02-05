import time
import logging
from abc import abstractmethod

from common.cmd.cmd_result import CmdResult
from common.cmd.cmd_status import CmdStatus

__author__ = 'itay.mizeretz'

logger = logging.getLogger(__name__)


class CmdRunner(object):
    """
    Interface for running a command on a remote machine
    """

    # Default command timeout in seconds
    DEFAULT_TIMEOUT = 5
    # Time to sleep when waiting on commands.
    WAIT_SLEEP_TIME = 1

    def __init__(self, is_linux):
        self.is_linux = is_linux

    def run_command(self, command, timeout=DEFAULT_TIMEOUT):
        """
        Runs the given command on the remote machine
        :param command: The command to run
        :param timeout: Timeout in seconds for command.
        :return: Command result
        """
        c_id = self.run_command_async(command)
        self.wait_commands([(self, c_id)], timeout)

    @abstractmethod
    def run_command_async(self, command):
        """
        Runs the given command on the remote machine asynchronously.
        :param command: The command to run
        :return: Command ID (in any format)
        """
        raise NotImplementedError()

    @staticmethod
    def wait_commands(commands, timeout=DEFAULT_TIMEOUT):
        """
        Waits on all commands up to given timeout
        :param commands: list of tuples of command IDs and command runners
        :param timeout: Timeout in seconds for command.
        :return: commands' results (tuple of
        """
        init_time = time.time()
        curr_time = init_time

        results = []

        while (curr_time - init_time < timeout) and (len(commands) != 0):
            for command in list(commands):
                CmdRunner._process_command(command, commands, results, True)

            time.sleep(CmdRunner.WAIT_SLEEP_TIME)
            curr_time = time.time()

        for command in list(commands):
            CmdRunner._process_command(command, commands, results, False)

        for command, result in results:
            if not result.is_success:
                logger.error('The following command failed: `%s`. status code: %s',
                             str(command[1]), str(result.status_code))

        return results

    @abstractmethod
    def query_command(self, command_id):
        """
        Queries the already run command for more info
        :param command_id: The command ID to query
        :return: Command info (in any format)
        """
        raise NotImplementedError()

    @abstractmethod
    def get_command_result(self, command_info):
        """
        Gets the result of the already run command
        :param command_info: The command info of the command to get the result of
        :return: CmdResult
        """
        raise NotImplementedError()

    @abstractmethod
    def get_command_status(self, command_info):
        """
        Gets the status of the already run command
        :param command_info: The command info of the command to get the result of
        :return: CmdStatus
        """
        raise NotImplementedError()

    @staticmethod
    def _process_command(command, commands, results, should_process_only_finished):
        """
        Removes the command from the list, processes its result and appends to results
        :param command:     Command to process. Must be in commands.
        :param commands:    List of unprocessed commands.
        :param results:     List of command results.
        :param should_process_only_finished: If True, processes only if command finished.
        :return: None
        """
        c_runner = command[0]
        c_id = command[1]
        try:
            command_info = c_runner.query_command(c_id)
            if (not should_process_only_finished) or c_runner.get_command_status(command_info) != CmdStatus.IN_PROGRESS:
                commands.remove(command)
                results.append((command, c_runner.get_command_result(command_info)))
        except Exception:
            logger.exception('Exception while querying command: `%s`', str(c_id))
            if not should_process_only_finished:
                commands.remove(command)
                results.append((command, CmdResult(False)))
