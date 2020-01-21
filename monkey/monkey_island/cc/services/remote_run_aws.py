import logging

from common.cloud.aws.aws_instance import AwsInstance
from common.cloud.aws.aws_service import AwsService
from common.cmd.aws.aws_cmd_runner import AwsCmdRunner
from common.cmd.cmd import Cmd
from common.cmd.cmd_runner import CmdRunner

__author__ = "itay.mizeretz"

logger = logging.getLogger(__name__)


class RemoteRunAwsService:
    aws_instance = None
    is_auth = False

    def __init__(self):
        pass

    @staticmethod
    def init():
        """
        Initializes service. Subsequent calls to this function have no effect.
        Must be called at least once (in entire monkey lifetime) before usage of functions
        :return: None
        """
        if RemoteRunAwsService.aws_instance is None:
            RemoteRunAwsService.try_init_aws_instance()

    @staticmethod
    def try_init_aws_instance():
        # noinspection PyBroadException
        try:
            RemoteRunAwsService.aws_instance = AwsInstance()
        except Exception:
            logger.error("Failed init aws instance. Exception info: ", exc_info=True)

    @staticmethod
    def run_aws_monkeys(instances, island_ip):
        """
        Runs monkeys on the given instances
        :param instances: List of instances to run on
        :param island_ip: IP of island the monkey will communicate with
        :return: Dictionary with instance ids as keys, and True/False as values if succeeded or not
        """
        instances_bitness = RemoteRunAwsService.get_bitness(instances)
        return CmdRunner.run_multiple_commands(
            instances,
            lambda instance: RemoteRunAwsService.run_aws_monkey_cmd_async(
                instance['instance_id'], RemoteRunAwsService._is_linux(instance['os']), island_ip,
                instances_bitness[instance['instance_id']]),
            lambda _, result: result.is_success)

    @staticmethod
    def is_running_on_aws():
        return RemoteRunAwsService.aws_instance.is_instance()

    @staticmethod
    def update_aws_region_authless():
        """
        Updates the AWS region without auth params (via IAM role)
        """
        AwsService.set_region(RemoteRunAwsService.aws_instance.region)

    @staticmethod
    def get_bitness(instances):
        """
        For all given instances, checks whether they're 32 or 64 bit.
        :param instances: List of instances to check
        :return: Dictionary with instance ids as keys, and True/False as values. True if 64bit, False otherwise
        """
        return CmdRunner.run_multiple_commands(
            instances,
            lambda instance: RemoteRunAwsService.run_aws_bitness_cmd_async(
                instance['instance_id'], RemoteRunAwsService._is_linux(instance['os'])),
            lambda instance, result: RemoteRunAwsService._get_bitness_by_result(
                RemoteRunAwsService._is_linux(instance['os']), result))

    @staticmethod
    def _get_bitness_by_result(is_linux, result):
        if not result.is_success:
            return None
        elif is_linux:
            return result.stdout.find('i686') == -1  # i686 means 32bit
        else:
            return result.stdout.lower().find('programfiles(x86)') != -1  # if not found it means 32bit

    @staticmethod
    def run_aws_bitness_cmd_async(instance_id, is_linux):
        """
        Runs an AWS command to check bitness
        :param instance_id: Instance ID of target
        :param is_linux:    Whether target is linux
        :return:            Cmd
        """
        cmd_text = 'uname -m' if is_linux else 'Get-ChildItem Env:'
        return RemoteRunAwsService.run_aws_cmd_async(instance_id, is_linux, cmd_text)

    @staticmethod
    def run_aws_monkey_cmd_async(instance_id, is_linux, island_ip, is_64bit):
        """
        Runs a monkey remotely using AWS
        :param instance_id: Instance ID of target
        :param is_linux:    Whether target is linux
        :param island_ip:   IP of the island which the instance will try to connect to
        :param is_64bit:    Whether the instance is 64bit
        :return:            Cmd
        """
        cmd_text = RemoteRunAwsService._get_run_monkey_cmd_line(is_linux, is_64bit, island_ip)
        return RemoteRunAwsService.run_aws_cmd_async(instance_id, is_linux, cmd_text)

    @staticmethod
    def run_aws_cmd_async(instance_id, is_linux, cmd_line):
        cmd_runner = AwsCmdRunner(is_linux, instance_id)
        return Cmd(cmd_runner, cmd_runner.run_command_async(cmd_line))

    @staticmethod
    def _is_linux(os):
        return 'linux' == os

    @staticmethod
    def _get_run_monkey_cmd_linux_line(bit_text, island_ip):
        return r'wget --no-check-certificate https://' + island_ip + r':5000/api/monkey/download/monkey-linux-' + \
               bit_text + r'; chmod +x monkey-linux-' + bit_text + r'; ./monkey-linux-' + bit_text + r' m0nk3y -s ' + \
               island_ip + r':5000'

    @staticmethod
    def _get_run_monkey_cmd_windows_line(bit_text, island_ip):
        return r"[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {" \
               r"$true}; (New-Object System.Net.WebClient).DownloadFile('https://" + island_ip + \
               r":5000/api/monkey/download/monkey-windows-" + bit_text + r".exe','.\\monkey.exe'); " \
                                                                         r";Start-Process -FilePath '.\\monkey.exe' " \
                                                                         r"-ArgumentList 'm0nk3y -s " + island_ip + r":5000'; "

    @staticmethod
    def _get_run_monkey_cmd_line(is_linux, is_64bit, island_ip):
        bit_text = '64' if is_64bit else '32'
        return RemoteRunAwsService._get_run_monkey_cmd_linux_line(bit_text, island_ip) if is_linux \
            else RemoteRunAwsService._get_run_monkey_cmd_windows_line(bit_text, island_ip)
