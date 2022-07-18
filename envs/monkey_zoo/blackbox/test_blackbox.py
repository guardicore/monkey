import logging
import os
from time import sleep

import pytest
from typing_extensions import Type

from envs.monkey_zoo.blackbox.analyzers.communication_analyzer import CommunicationAnalyzer
from envs.monkey_zoo.blackbox.analyzers.zerologon_analyzer import ZerologonAnalyzer
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate
from envs.monkey_zoo.blackbox.config_templates.depth_1_a import Depth1A
from envs.monkey_zoo.blackbox.config_templates.depth_2_a import Depth2A
from envs.monkey_zoo.blackbox.config_templates.depth_3_a import Depth3A
from envs.monkey_zoo.blackbox.config_templates.powershell_credentials_reuse import (
    PowerShellCredentialsReuse,
)
from envs.monkey_zoo.blackbox.config_templates.smb_pth import SmbPth
from envs.monkey_zoo.blackbox.config_templates.wmi_mimikatz import WmiMimikatz
from envs.monkey_zoo.blackbox.config_templates.zerologon import Zerologon
from envs.monkey_zoo.blackbox.gcp_test_machine_list import GCP_TEST_MACHINE_LIST
from envs.monkey_zoo.blackbox.island_client.island_config_parser import IslandConfigParser
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient
from envs.monkey_zoo.blackbox.log_handlers.test_logs_handler import TestLogsHandler
from envs.monkey_zoo.blackbox.tests.exploitation import ExploitationTest
from envs.monkey_zoo.blackbox.utils.gcp_machine_handlers import (
    initialize_gcp_client,
    start_machines,
    stop_machines,
)
from monkey_island.cc.services.mode.mode_enum import IslandModeEnum

DEFAULT_TIMEOUT_SECONDS = 2 * 60 + 30
MACHINE_BOOTUP_WAIT_SECONDS = 30
LOG_DIR_PATH = "./logs"
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@pytest.fixture(autouse=True, scope="session")
def GCPHandler(request, no_gcp):
    if not no_gcp:
        try:
            initialize_gcp_client()
            start_machines(GCP_TEST_MACHINE_LIST)
        except Exception as e:
            LOGGER.error("GCP Handler failed to initialize: %s." % e)
            pytest.exit("Encountered an error while starting GCP machines. Stopping the tests.")
        wait_machine_bootup()

        def fin():
            stop_machines(GCP_TEST_MACHINE_LIST)

        request.addfinalizer(fin)


@pytest.fixture(autouse=True, scope="session")
def delete_logs():
    LOGGER.info("Deleting monkey logs before new tests.")
    TestLogsHandler.delete_log_folder_contents(TestMonkeyBlackbox.get_log_dir_path())


def wait_machine_bootup():
    sleep(MACHINE_BOOTUP_WAIT_SECONDS)


@pytest.fixture(scope="class")
def island_client(island, quick_performance_tests):
    client_established = False
    try:
        island_client_object = MonkeyIslandClient(island)
        client_established = island_client_object.get_api_status()
    except Exception:
        logging.exception("Got an exception while trying to establish connection to the Island.")
    finally:
        if not client_established:
            pytest.exit("BB tests couldn't establish communication to the island.")
    if not quick_performance_tests:
        island_client_object.reset_env()
        island_client_object.set_scenario(IslandModeEnum.ADVANCED.value)
    yield island_client_object


@pytest.mark.usefixtures("island_client")
# noinspection PyUnresolvedReferences
class TestMonkeyBlackbox:
    @staticmethod
    def run_exploitation_test(
        island_client: MonkeyIslandClient,
        config_template: Type[ConfigTemplate],
        test_name: str,
        timeout_in_seconds=DEFAULT_TIMEOUT_SECONDS,
    ):
        raw_config = IslandConfigParser.get_raw_config(config_template, island_client)
        analyzer = CommunicationAnalyzer(
            island_client, IslandConfigParser.get_ips_of_targets(raw_config)
        )
        log_handler = TestLogsHandler(
            test_name, island_client, TestMonkeyBlackbox.get_log_dir_path()
        )
        ExploitationTest(
            name=test_name,
            island_client=island_client,
            raw_config=raw_config,
            analyzers=[analyzer],
            timeout=timeout_in_seconds,
            log_handler=log_handler,
        ).run()

    @staticmethod
    def get_log_dir_path():
        return os.path.abspath(LOG_DIR_PATH)

    # If test_depth_1_a() is run first, some test will fail because machines are not yet fully
    # booted. Running test_depth_2_a() first gives slow VMs extra time to boot.
    def test_depth_2_a(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, Depth2A, "Depth2A test suite")

    def test_depth_1_a(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, Depth1A, "Depth1A test suite")

    def test_depth_3_a(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, Depth3A, "Depth3A test suite")

    # Not grouped because can only be ran on windows
    @pytest.mark.skip_powershell_reuse
    def test_powershell_exploiter_credentials_reuse(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client,
            PowerShellCredentialsReuse,
            "PowerShell_Remoting_exploiter_credentials_reuse",
        )

    # Not grouped because it's slow
    def test_zerologon_exploiter(self, island_client):
        test_name = "Zerologon_exploiter"
        expected_creds = [
            "Administrator",
            "aad3b435b51404eeaad3b435b51404ee",
            "2864b62ea4496934a5d6e86f50b834a5",
        ]
        raw_config = IslandConfigParser.get_raw_config(Zerologon, island_client)
        zero_logon_analyzer = ZerologonAnalyzer(island_client, expected_creds)
        communication_analyzer = CommunicationAnalyzer(
            island_client, IslandConfigParser.get_ips_of_targets(raw_config)
        )
        log_handler = TestLogsHandler(
            test_name, island_client, TestMonkeyBlackbox.get_log_dir_path()
        )
        ExploitationTest(
            name=test_name,
            island_client=island_client,
            raw_config=raw_config,
            analyzers=[zero_logon_analyzer, communication_analyzer],
            timeout=DEFAULT_TIMEOUT_SECONDS + 30,
            log_handler=log_handler,
        ).run()

    # Not grouped because conflicts with SMB.
    # Consider grouping when more depth 1 exploiters collide with group depth_1_a
    def test_wmi_and_mimikatz_exploiters(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, WmiMimikatz, "WMI_exploiter,_mimikatz"
        )

    # Not grouped because it's depth 1 but conflicts with SMB exploiter in group depth_1_a
    def test_smb_pth(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, SmbPth, "SMB_PTH")
