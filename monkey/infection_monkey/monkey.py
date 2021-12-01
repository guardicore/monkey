import argparse
import logging
import os
import subprocess
import sys

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
from infection_monkey.utils.exceptions.planned_shutdown_error import PlannedShutdownError
from infection_monkey.utils.monkey_dir import get_monkey_dir_path, remove_monkey_dir
from infection_monkey.utils.monkey_log_path import get_monkey_log_path
from infection_monkey.utils.signal_handler import register_signal_handlers
from infection_monkey.windows_upgrader import WindowsUpgrader

logger = logging.getLogger(__name__)


class PlannedShutdownError(Exception):
    # Raise when we deliberately want to shut down the agent
    pass


class InfectionMonkey:
    def __init__(self, args):
        logger.info("Monkey is initializing...")
        self._master = MockMaster(MockPuppet(), LegacyTelemetryMessengerAdapter())
        self._singleton = SystemSingleton()
        self._opts = None
        self._set_arguments(args)
        self._parent = self._opts.parent
        self._default_tunnel = self._opts.tunnel
        self._default_server = self._opts.server
        self._default_server_port = None
        self._set_propagation_depth()
        self._add_default_server_to_config()
        self._monkey_tunnel = None

    def _set_arguments(self, args):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("-p", "--parent")
        arg_parser.add_argument("-t", "--tunnel")
        arg_parser.add_argument("-s", "--server")
        arg_parser.add_argument("-d", "--depth", type=int)
        arg_parser.add_argument("-vp", "--vulnerable-port")
        self._opts, _ = arg_parser.parse_known_args(args)
        self._log_arguments()

    def _log_arguments(self):
        arg_string = " ".join([f"{key}: {value}" for key, value in vars(self._opts).items()])
        logger.info(f"Monkey started with arguments: {arg_string}")

    def _set_propagation_depth(self):
        if self._opts.depth is not None:
            WormConfiguration._depth_from_commandline = True
            WormConfiguration.depth = self._opts.depth
            logger.debug("Setting propagation depth from command line")
        logger.debug(f"Set propagation depth to {WormConfiguration.depth}")

    def _add_default_server_to_config(self):
        if self._default_server:
            if self._default_server not in WormConfiguration.command_servers:
                logger.debug("Added default server: %s" % self._default_server)
                WormConfiguration.command_servers.insert(0, self._default_server)
            else:
                logger.debug(
                    "Default server: %s is already in command servers list" % self._default_server
                )

    def start(self):
        if self._is_another_monkey_running():
            raise PlannedShutdownError("Another instance of the monkey is already running.")

        logger.info("Monkey is starting...")

        self._connect_to_island()

        # TODO: Reevaluate who is responsible to send this information
        if is_windows_os():
            T1106Telem(ScanStatus.USED, UsageEnum.SINGLETON_WINAPI).send()

        if InfectionMonkey._is_monkey_alive_by_config():
            raise PlannedShutdownError("Monkey marked 'not alive' from configuration.")

        if InfectionMonkey._is_upgrade_to_64_needed():
            self._upgrade_to_64()
            raise PlannedShutdownError("32 bit Agent can't run on 64 bit system.")

        self._setup()
        self._master.start()

    def _connect_to_island(self):
        # Sets island's IP and port for monkey to communicate to
        if not self._is_default_server_set():
            raise Exception(
                "Monkey couldn't find server with {} default tunnel.".format(self._default_tunnel)
            )
        self._set_default_port()

        ControlClient.wakeup(parent=self._parent)
        ControlClient.load_control_config()

    def _is_default_server_set(self) -> bool:
        """
        Sets the default server for the Monkey to communicate back to.
        :return
        """
        if not ControlClient.find_server(default_tunnel=self._default_tunnel):
            return False
        self._default_server = WormConfiguration.current_server
        logger.debug("default server set to: %s" % self._default_server)
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

        self._should_run_check_for_performance()

        if firewall.is_enabled():
            firewall.add_firewall_rule()

        self._monkey_tunnel = ControlClient.create_control_tunnel()
        if self._monkey_tunnel:
            self._monkey_tunnel.start()

        StateTelem(is_done=False, version=get_version()).send()
        TunnelTelem().send()

        register_signal_handlers(self._master)

    def _should_run_check_for_performance(self):
        """
        This method implements propagation performance enhancing algorithm that
        kicks in if the run was started from the Island.
        Should get replaced by other, better performance enhancement solutions
        """
        if is_running_on_island():
            WormConfiguration.started_on_island = True
            ControlClient.report_start_on_island()

        if not ControlClient.should_monkey_run(self._opts.vulnerable_port):
            raise PlannedShutdownError(
                "Monkey shouldn't run on current machine to improve perfomance"
                "(it will be exploited later with more depth)."
            )

    def _is_another_monkey_running(self):
        return not self._singleton.try_lock()

    def _set_default_port(self):
        try:
            self._default_server_port = self._default_server.split(":")[1]
        except KeyError:
            self._default_server_port = ""

    def cleanup(self):
        logger.info("Monkey cleanup started")
        try:
            if self._is_upgrade_to_64_needed():
                logger.debug("Detected upgrade to 64bit")
                return

            if self._master:
                self._master.cleanup()

            if self._monkey_tunnel:
                self._monkey_tunnel.stop()
                self._monkey_tunnel.join()

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
