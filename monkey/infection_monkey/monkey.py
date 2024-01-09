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
from multiprocessing.managers import SyncManager
from pathlib import Path, WindowsPath
from tempfile import gettempdir
from typing import Optional, Sequence, Tuple

from monkeyevents import (
    AgentEventTag,
    AgentShutdownEvent,
    CredentialsStolenEvent,
    HostnameDiscoveryEvent,
    OSDiscoveryEvent,
    PropagationEvent,
)
from monkeyevents.tags.attack import SYSTEM_INFORMATION_DISCOVERY_T1082_TAG
from monkeytoolbox import (
    create_secure_directory,
    del_key,
    get_binary_io_sha256_hash,
    get_hostname,
    get_my_ip_addresses,
    get_network_interfaces,
    get_os,
    get_os_version,
    secure_generate_random_string,
)
from monkeytypes import OTP, AgentPluginType, NetworkPort, OperatingSystem, SocketAddress
from pubsub.core import Publisher
from serpentarium import PluginLoader, PluginThreadName
from serpentarium.logging import configure_child_process_logger

from common.agent_events import (
    AgentEventSerializerRegistry,
    register_builtin_agent_event_serializers,
)
from common.agent_registration_data import AgentRegistrationData
from common.common_consts import AGENT_OTP_ENVIRONMENT_VARIABLE
from common.event_queue import IAgentEventQueue, PyPubSubAgentEventQueue, QueuedAgentEventPublisher
from infection_monkey.agent_event_handlers import (
    AgentEventForwarder,
    add_stolen_credentials_to_propagation_credentials_repository,
    notify_relay_on_propagation,
)
from infection_monkey.exploit import (
    CachingAgentBinaryRepository,
    IAgentBinaryRepository,
    IslandAPIAgentOTPProvider,
    PolymorphicAgentBinaryRepositoryDecorator,
)
from infection_monkey.exploit.http_agent_binary_request_handler import ThreadingHTTPHandlerFactory
from infection_monkey.exploit.http_agent_binary_server import HTTPAgentBinaryServer
from infection_monkey.exploit.http_agent_binary_server_factory import HTTPAgentBinaryServerFactory
from infection_monkey.exploit.http_agent_binary_server_registrar import (
    HTTPAgentBinaryServerRegistrar,
)
from infection_monkey.i_master import IMaster
from infection_monkey.i_puppet import IPuppet
from infection_monkey.island_api_client import (
    HTTPIslandAPIClientFactory,
    IIslandAPIClient,
    IslandAPIAuthenticationError,
    IslandAPIError,
)
from infection_monkey.local_machine_info import LocalMachineInfo
from infection_monkey.master import AutomatedMaster
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
from infection_monkey.plugin.credentials_collector_plugin_factory import (
    CredentialsCollectorPluginFactory,
)
from infection_monkey.plugin.exploiter_plugin_factory import ExploiterPluginFactory
from infection_monkey.plugin.multiprocessing_plugin_wrapper import MultiprocessingPluginWrapper
from infection_monkey.plugin.payload_plugin_factory import PayloadPluginFactory
from infection_monkey.propagation_credentials_repository import PropagationCredentialsRepository
from infection_monkey.puppet import (
    PluginCompatibilityVerifier,
    PluginRegistry,
    PluginSourceExtractor,
)
from infection_monkey.puppet.puppet import Puppet
from infection_monkey.utils import agent_process
from infection_monkey.utils.argparse_types import positive_int
from infection_monkey.utils.file_utils import mark_file_for_deletion_on_windows
from infection_monkey.utils.ids import get_agent_id, get_machine_id
from infection_monkey.utils.monkey_dir import (
    create_monkey_dir,
    get_monkey_dir_path,
    remove_monkey_dir,
)
from infection_monkey.utils.propagation import maximum_depth_reached
from infection_monkey.utils.signal_handler import register_signal_handlers, reset_signal_handlers

from .heart import Heart
from .plugin_event_forwarder import PluginEventForwarder

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.INFO)


class InfectionMonkey:
    def __init__(self, args, ipc_logger_queue: multiprocessing.Queue, log_path: Path):
        logger.info("Agent is initializing...")

        self._agent_id = get_agent_id()
        self._log_path = log_path
        self._running_from_source = "python" in Path(sys.executable).name
        self._sha256 = self._calculate_agent_sha256_hash()
        logger.info(f"Agent ID: {self._agent_id}")
        logger.info(f"Process ID: {os.getpid()}")
        logger.info(f"SHA256: {self._sha256}")

        context = multiprocessing.get_context("spawn")

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

        http_island_api_client_factory = HTTPIslandAPIClientFactory(
            self._agent_event_serializer_registry, self._agent_id, context.Lock()
        )
        # Register a proxy for HTTPIslandAPIClient. The manager will create and own the instance
        SyncManager.register(
            "HTTPIslandAPIClient", http_island_api_client_factory.create_island_api_client
        )
        SyncManager.register(
            "HTTPAgentBinaryServerFactory", HTTPAgentBinaryServerFactory, exposed=("__call__",)
        )
        SyncManager.register("TCPPortSelector", TCPPortSelector)
        self._manager = context.Manager()
        self._plugin_dir = (
            Path(gettempdir())
            / f"infection_monkey_plugins_{self._agent_id}_{secure_generate_random_string(n=20)}"
        )

        self._local_machine_info = LocalMachineInfo(
            operating_system=get_os(),
            temporary_directory=get_monkey_dir_path(),
            network_interfaces=get_network_interfaces(),
        )

        self._island_address, self._island_api_client = self._connect_to_island_api()
        self._register_agent()

        self._propagation_credentials_repository = PropagationCredentialsRepository(
            self._island_api_client, self._manager
        )

        self._heart = Heart(self._island_api_client)
        self._heart.start()

        self._current_depth = self._opts.depth
        self._master: Optional[IMaster] = None
        self._relay: Optional[TCPRelay] = None
        self._tcp_port_selector = self._manager.TCPPortSelector()  # type: ignore[attr-defined]

    def _calculate_agent_sha256_hash(self) -> str:
        sha256 = "0" * 64

        if self._running_from_source:
            return sha256

        try:
            with open(sys.executable, "rb") as f:
                sha256 = get_binary_io_sha256_hash(f)
        except Exception:
            logger.exception(
                "An error occurred while attempting to calculate the agent binary's SHA256 hash."
            )

        logger.info(f"Agent Binary SHA256: {sha256}")
        return sha256

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
        try:
            otp = OTP(os.environ[AGENT_OTP_ENVIRONMENT_VARIABLE])
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

        server, island_api_client = self._select_server(server_clients, self._manager)

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
        self, island_api_statuses: IslandAPISearchResults, manager: SyncManager
    ) -> Tuple[Optional[SocketAddress], Optional[IIslandAPIClient]]:
        for server in self._opts.servers:
            if island_api_statuses[server]:
                try:
                    island_api_client = manager.HTTPIslandAPIClient(  # type: ignore[attr-defined]
                        server
                    )
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
            network_interfaces=self._local_machine_info.network_interfaces,
            sha256=self._sha256,
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
        if self._island_api_client.terminate_signal_is_set():
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
        operating_system = get_os()
        operating_system_version = get_os_version()

        event = OSDiscoveryEvent(
            source=self._agent_id,
            timestamp=timestamp,
            tags=frozenset({AgentEventTag(SYSTEM_INFORMATION_DISCOVERY_T1082_TAG)}),
            os=operating_system,
            version=operating_system_version,
        )
        self._agent_event_queue.publish(event)

        return operating_system

    def _discover_hostname(self):
        timestamp = time.time()
        hostname = get_hostname()

        event = HostnameDiscoveryEvent(
            source=self._agent_id,
            timestamp=timestamp,
            tags={SYSTEM_INFORMATION_DISCOVERY_T1082_TAG},
            hostname=hostname,
        )
        self._agent_event_queue.publish(event)

    def _setup(self, operating_system: OperatingSystem):
        logger.debug("Starting the setup phase.")

        create_monkey_dir()

        if firewall.is_enabled():
            firewall.add_firewall_rule()

        config = self._island_api_client.get_config()

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
        register_builtin_agent_event_serializers(agent_event_serializer_registry)

        return agent_event_serializer_registry

    def _build_master(self, servers: Sequence[str], operating_system: OperatingSystem) -> IMaster:
        puppet = self._build_puppet(operating_system)

        return AutomatedMaster(
            self._current_depth,
            servers,
            puppet,
            self._island_api_client,
            self._local_machine_info.network_interfaces,
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

        agent_binary_repository = self._build_agent_binary_repository()

        plugin_source_extractor = PluginSourceExtractor(self._plugin_dir)
        plugin_loader = PluginLoader(
            self._plugin_dir, partial(configure_child_process_logger, self._ipc_logger_queue)
        )
        otp_provider = IslandAPIAgentOTPProvider(self._island_api_client)
        create_plugin = partial(
            MultiprocessingPluginWrapper,
            plugin_loader=plugin_loader,
            reset_modules_cache=False,
            main_thread_name=PluginThreadName.CALLING_THREAD,
        )

        http_agent_binary_server = self._build_http_agent_binary_server(agent_binary_repository)
        http_agent_binary_server_registrar = HTTPAgentBinaryServerRegistrar(
            http_agent_binary_server
        )

        plugin_factories = {
            AgentPluginType.CREDENTIALS_COLLECTOR: CredentialsCollectorPluginFactory(
                self._agent_id, self._agent_event_publisher, self._local_machine_info, create_plugin
            ),
            AgentPluginType.EXPLOITER: ExploiterPluginFactory(
                self._agent_id,
                http_agent_binary_server_registrar,
                agent_binary_repository,
                self._agent_event_publisher,
                self._propagation_credentials_repository,
                self._tcp_port_selector,
                otp_provider,
                AGENT_OTP_ENVIRONMENT_VARIABLE,
                self._local_machine_info,
                create_plugin,
            ),
            AgentPluginType.PAYLOAD: PayloadPluginFactory(
                self._agent_id,
                self._agent_event_publisher,
                self._island_address,
                self._local_machine_info,
                create_plugin,
            ),
        }
        plugin_registry = PluginRegistry(
            operating_system,
            self._island_api_client,
            plugin_source_extractor,
            plugin_factories,
        )
        plugin_compatibility_verifier = PluginCompatibilityVerifier(
            self._island_api_client,
            self._local_machine_info.operating_system,
        )

        puppet = Puppet(
            agent_event_queue=self._agent_event_queue,
            plugin_registry=plugin_registry,
            plugin_compatibility_verifier=plugin_compatibility_verifier,
            agent_id=self._agent_id,
        )

        puppet.load_plugin(
            AgentPluginType.FINGERPRINTER,
            "http",
            HTTPFingerprinter(self._agent_id, self._agent_event_publisher),
        )
        puppet.load_plugin(
            AgentPluginType.FINGERPRINTER,
            "mssql",
            MSSQLFingerprinter(self._agent_id, self._agent_event_publisher),
        )
        puppet.load_plugin(
            AgentPluginType.FINGERPRINTER,
            "smb",
            SMBFingerprinter(self._agent_id, self._agent_event_publisher),
        )
        puppet.load_plugin(
            AgentPluginType.FINGERPRINTER,
            "ssh",
            SSHFingerprinter(self._agent_id, self._agent_event_publisher),
        )

        return puppet

    def _build_agent_binary_repository(self) -> IAgentBinaryRepository:
        agent_configuration = self._island_api_client.get_config()
        agent_binary_repository: IAgentBinaryRepository = CachingAgentBinaryRepository(
            island_api_client=self._island_api_client,
            manager=self._manager,
        )

        if agent_configuration.polymorphism.randomize_agent_hash:
            agent_binary_repository = PolymorphicAgentBinaryRepositoryDecorator(
                agent_binary_repository
            )

        return agent_binary_repository

    def _build_http_agent_binary_server(
        self, agent_binary_repository: IAgentBinaryRepository
    ) -> HTTPAgentBinaryServer:
        server_factory = self._manager.HTTPAgentBinaryServerFactory(  # type: ignore[attr-defined]
            self._local_machine_info,
            self._tcp_port_selector,
            agent_binary_repository,
            ThreadingHTTPHandlerFactory,
        )
        return server_factory()

    def _subscribe_events(self):
        self._agent_event_queue.subscribe_type(
            CredentialsStolenEvent,
            add_stolen_credentials_to_propagation_credentials_repository(
                self._propagation_credentials_repository,
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

            deleted = self._self_delete()

            self._send_log()

            self._publish_agent_shutdown_event()

            self._plugin_event_forwarder.flush()

            if self._agent_event_forwarder:
                self._agent_event_forwarder.flush()

            self._heart.stop()

            self._logout()

            self._close_tunnel()

        except Exception as e:
            logger.exception(f"An error occurred while cleaning up the monkey agent: {e}")
            if deleted is None:
                self._self_delete()
        finally:
            self._plugin_event_forwarder.stop()
            if self._agent_event_forwarder:
                self._agent_event_forwarder.stop()
            self._delete_plugin_dir()
            self._manager.shutdown()

        logger.info("Agent is shutting down")

    def _stop_relay(self):
        if not self._relay or not self._relay.is_alive():
            return

        self._relay.stop()

        try:
            while self._relay.is_alive() and not self._island_api_client.terminate_signal_is_set():
                self._relay.join(timeout=5)

            if self._island_api_client.terminate_signal_is_set():
                self._relay.join(timeout=60)
        except IslandAPIError as err:
            logger.warning(f"Error communicating with the Island: {err}")
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

    def _self_delete(self) -> bool:
        logger.info("Cleaning up the Agent's artifacts")
        remove_monkey_dir()

        if self._running_from_source:
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

    def _logout(self):
        try:
            self._island_api_client.logout()
        except IslandAPIAuthenticationError:
            logger.info("Agent is already logged out")
