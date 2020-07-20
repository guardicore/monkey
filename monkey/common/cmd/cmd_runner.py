import logging
import time
from abc import abstractmethod

from common.cmd.cmd import Cmd
from common.cmd.cmd_result import CmdResult
from common.cmd.cmd_status import CmdStatus

__author__ = 'itay.mizeretz'

logger = logging.getLogger(__name__)


class CmdRunner(object):
    """
    Interface for running commands on a remote machine

    Since these classes are a bit complex, I provide a list of common terminology and formats:
    * command line - a command line. e.g. 'echo hello'
    * command - represent a single command which was already run. Always of type Cmd
    * command id - any unique identifier of a command which was already run
    * command result - represents the result of running a command. Always of type CmdResult
    * command status - represents the current status of a command. Always of type CmdStatus
    * command info - Any consistent structure representing additional information of a command which was already run
    * instance - a machine that commands will be run on. Can be any dictionary with 'instance_id' as a field
    * instance_id - any unique identifier of an instance (machine). Can be of any format
    """

    # Default command timeout in seconds
    DEFAULT_TIMEOUT = 5
    # Time to sleep when waiting on commands.
    WAIT_SLEEP_TIME = 1

    def __init__(self, is_linux):
        self.is_linux = is_linux

    def run_command(self, command_line, timeout=DEFAULT_TIMEOUT):
        """
        Runs the given command on the remote machine
        :param command_line: The command line to run
        :param timeout: Timeout in seconds for command.
        :return: Command result
        """
        c_id = self.run_command_async(command_line)
        return self.wait_commands([Cmd(self, c_id)], timeout)[1]

    @staticmethod
    def run_multiple_commands(instances, inst_to_cmd, inst_n_cmd_res_to_res):
        """
        Run multiple commands on various instances
        :param instances:   List of instances.
        :param inst_to_cmd: Function which receives an instance, runs a command asynchronously and returns Cmd
        :param inst_n_cmd_res_to_res:   Function which receives an instance and CmdResult
                                        and returns a parsed result (of any format)
        :return: Dictionary with 'instance_id' as key and parsed result as value
        """
        command_instance_dict = {}

        for instance in instances:
            command = inst_to_cmd(instance)
            command_instance_dict[command] = instance

        instance_results = {}
        command_result_pairs = CmdRunner.wait_commands(list(command_instance_dict.keys()))
        for command, result in command_result_pairs:
            instance = command_instance_dict[command]
            instance_results[instance['instance_id']] = inst_n_cmd_res_to_res(instance, result)

        return instance_results

    @abstractmethod
    def run_command_async(self, command_line):
        """
        Runs the given command on the remote machine asynchronously.
        :param command_line: The command line to run
        :return: Command ID (in any format)
        """
        raise NotImplementedError()

    @staticmethod
    def wait_commands(commands, timeout=DEFAULT_TIMEOUT):
        """
        Waits on all commands up to given timeout
        :param commands: list of commands (of type Cmd)
        :param timeout: Timeout in seconds for command.
        :return: commands and their results (tuple of Command and CmdResult)
        """
        init_time = time.time()
        curr_time = init_time

        results = []

        while (curr_time - init_time < timeout) and (len(commands) != 0):
            for command in list(commands):  # list(commands) clones the list. We do so because we remove items inside
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
        c_runner = command.cmd_runner
        c_id = command.cmd_id
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
