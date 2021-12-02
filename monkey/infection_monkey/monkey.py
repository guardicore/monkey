import argparse
import logging
import os
import subprocess
import sys
import time

import infection_monkey.tunnel as tunnel
from common.utils.attack_utils import ScanStatus, UsageEnum
from common.version import get_version
from infection_monkey.config import WormConfiguration
from infection_monkey.control import ControlClient
from infection_monkey.master.mock_master import MockMaster
from infection_monkey.model import DELAY_DELETE_CMD
from infection_monkey.network.firewall import app as firewall
from infection_monkey.network.tools import is_running_on_island
from infection_monkey.puppet.mock_puppet import MockPuppet
from infection_monkey.system_singleton import SystemSingleton
from infection_monkey.telemetry.attack.t1106_telem import T1106Telem
from infection_monkey.telemetry.attack.t1107_telem import T1107Telem
from infection_monkey.telemetry.messengers.legacy_telemetry_messenger_adapter import (
    LegacyTelemetryMessengerAdapter,
)
from infection_monkey.telemetry.state_telem import StateTelem
from infection_monkey.telemetry.tunnel_telem import TunnelTelem
from infection_monkey.utils.environment import is_windows_os
from infection_monkey.utils.monkey_dir import get_monkey_dir_path, remove_monkey_dir
from infection_monkey.utils.monkey_log_path import get_monkey_log_path
from infection_monkey.utils.signal_handler import register_signal_handlers
from infection_monkey.windows_upgrader import WindowsUpgrader

logger = logging.getLogger(__name__)


class InfectionMonkey:
    def __init__(self, args):
        logger.info("Monkey is initializing...")
        self._master = MockMaster(MockPuppet(), LegacyTelemetryMessengerAdapter())
        self._singleton = SystemSingleton()
        self._opts = self._get_arguments(args)
        # TODO Used in propagation phase to set the default server for the victim
        self._default_server_port = None
        # TODO used in propogation phase
        self._monkey_inbound_tunnel = None

    @staticmethod
    def _get_arguments(args):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("-p", "--parent")
        arg_parser.add_argument("-t", "--tunnel")
        arg_parser.add_argument("-s", "--server")
        arg_parser.add_argument("-d", "--depth", type=int)
        arg_parser.add_argument("-vp", "--vulnerable-port")
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

        self._set_propagation_depth(self._opts)
        self._add_default_server_to_config(self._opts.server)
        self._connect_to_island()

        # TODO: Reevaluate who is responsible to send this information
        if is_windows_os():
            T1106Telem(ScanStatus.USED, UsageEnum.SINGLETON_WINAPI).send()

        if InfectionMonkey._is_monkey_alive_by_config():
            logger.info("Monkey marked 'not alive' from configuration.")
            return

        if InfectionMonkey._is_upgrade_to_64_needed():
            self._upgrade_to_64()
            logger.info("32 bit Agent can't run on 64 bit system.")
            return

        self._setup()
        self._master.start()

    @staticmethod
    def _set_propagation_depth(options):
        if options.depth is not None:
            WormConfiguration._depth_from_commandline = True
            WormConfiguration.depth = options.depth
            logger.debug("Setting propagation depth from command line")
        logger.debug(f"Set propagation depth to {WormConfiguration.depth}")

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
        if not self._is_default_server_set():
            raise Exception(
                "Monkey couldn't find server with {} default tunnel.".format(self._opts.tunnel)
            )
        self._set_default_port()

        ControlClient.wakeup(parent=self._opts.parent)
        ControlClient.load_control_config()

    def _is_default_server_set(self) -> bool:
        """
        Sets the default server for the Monkey to communicate back to.
        :return
        """
        if not ControlClient.find_server(default_tunnel=self._opts.tunnel):
            return False
        self._opts.server = WormConfiguration.current_server
        logger.debug("default server set to: %s" % self._opts.server)
        return True

    @staticmethod
    def _is_monkey_alive_by_config():
        return not WormConfiguration.alive

    @staticmethod
    def _is_upgrade_to_64_needed():
        return WindowsUpgrader.should_upgrade()

    def _upgrade_to_64(self):
        self._singleton.unlock()
        logger.info("32bit monkey running on 64bit Windows. Upgrading.")
        WindowsUpgrader.upgrade(self._opts)
        logger.info("Finished upgrading from 32bit to 64bit.")

    def _setup(self):
        logger.debug("Starting the setup phase.")

        if self._should_exit_for_performance():
            logger.info(
                "Monkey shouldn't run on current machine to improve perfomance"
                "(it will be exploited later with more depth)."
            )
            return

        if firewall.is_enabled():
            firewall.add_firewall_rule()

        self._monkey_inbound_tunnel = ControlClient.create_control_tunnel()
        if self._monkey_inbound_tunnel:
            self._monkey_inbound_tunnel.start()

        StateTelem(is_done=False, version=get_version()).send()
        TunnelTelem().send()

        register_signal_handlers(self._master)

    def _should_exit_for_performance(self):
        """
        This method implements propagation performance enhancing algorithm that
        kicks in if the run was started from the Island.
        Should get replaced by other, better performance enhancement solutions
        """
        if is_running_on_island():
            WormConfiguration.started_on_island = True
            ControlClient.report_start_on_island()

        return not ControlClient.should_monkey_run(self._opts.vulnerable_port)

    def _is_another_monkey_running(self):
        return not self._singleton.try_lock()

    def _set_default_port(self):
        try:
            self._default_server_port = self._opts.server.split(":")[1]
        except KeyError:
            self._default_server_port = ""

    def cleanup(self):
        logger.info("Monkey cleanup started")
        self._wait_for_exploited_machine_connection()
        try:
            if self._is_upgrade_to_64_needed():
                logger.debug("Cleanup not needed for 32 bit agent on 64 bit system(it didn't run)")
                return

            if self._master:
                self._master.cleanup()

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

    def _wait_for_exploited_machine_connection(self):
        # TODO check for actual exploitation
        machines_exploited = False
        # if host was exploited, before continue to closing the tunnel ensure the exploited
        # host had its chance to
        # connect to the tunnel
        if machines_exploited:
            time_to_sleep = WormConfiguration.keep_tunnel_open_time
            logger.info(
                "Sleeping %d seconds for exploited machines to connect to tunnel", time_to_sleep
            )
            time.sleep(time_to_sleep)

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
        monkey_log_path = get_monkey_log_path()
        if os.path.exists(monkey_log_path):
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
