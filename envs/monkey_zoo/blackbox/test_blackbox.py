import logging
import os
from time import sleep

import pytest

from envs.monkey_zoo.blackbox.analyzers.communication_analyzer import CommunicationAnalyzer
from envs.monkey_zoo.blackbox.analyzers.zerologon_analyzer import ZerologonAnalyzer
from envs.monkey_zoo.blackbox.gcp_test_machine_list import GCP_TEST_MACHINE_LIST
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient
from envs.monkey_zoo.blackbox.island_client.test_configuration_parser import TestConfigurationParser
from envs.monkey_zoo.blackbox.log_handlers.test_logs_handler import TestLogsHandler
from envs.monkey_zoo.blackbox.test_configurations import (
    depth_1_a_test_configuration,
    depth_2_a_test_configuration,
    depth_3_a_test_configuration,
    powershell_credentials_reuse_test_configuration,
    smb_pth_test_configuration,
    wmi_mimikatz_test_configuration,
    zerologon_test_configuration,
)
from envs.monkey_zoo.blackbox.test_configurations.test_configuration import TestConfiguration
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
        test_configuration: TestConfiguration,
        test_name: str,
        timeout_in_seconds=DEFAULT_TIMEOUT_SECONDS,
    ):
        analyzer = CommunicationAnalyzer(
            island_client,
            TestConfigurationParser.get_target_ips(test_configuration),
        )
        log_handler = TestLogsHandler(
            test_name, island_client, TestMonkeyBlackbox.get_log_dir_path()
        )
        ExploitationTest(
            name=test_name,
            island_client=island_client,
            test_configuration=test_configuration,
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
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, depth_2_a_test_configuration, "Depth2A test suite"
        )

    def test_depth_1_a(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, depth_1_a_test_configuration, "Depth1A test suite"
        )

    def test_depth_3_a(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, depth_3_a_test_configuration, "Depth3A test suite"
        )

    # Not grouped because can only be ran on windows
    @pytest.mark.skip_powershell_reuse
    def test_powershell_exploiter_credentials_reuse(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client,
            powershell_credentials_reuse_test_configuration,
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
        zero_logon_analyzer = ZerologonAnalyzer(island_client, expected_creds)
        communication_analyzer = CommunicationAnalyzer(
            island_client,
            TestConfigurationParser.get_target_ips(zerologon_test_configuration),
        )
        log_handler = TestLogsHandler(
            test_name, island_client, TestMonkeyBlackbox.get_log_dir_path()
        )
        ExploitationTest(
            name=test_name,
            island_client=island_client,
            test_configuration=zerologon_test_configuration,
            analyzers=[zero_logon_analyzer, communication_analyzer],
            timeout=DEFAULT_TIMEOUT_SECONDS + 30,
            log_handler=log_handler,
        ).run()

    # Not grouped because conflicts with SMB.
    # Consider grouping when more depth 1 exploiters collide with group depth_1_a
    def test_wmi_and_mimikatz_exploiters(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, wmi_mimikatz_test_configuration, "WMI_exploiter,_mimikatz"
        )

    # Not grouped because it's depth 1 but conflicts with SMB exploiter in group depth_1_a
    def test_smb_pth(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, smb_pth_test_configuration, "SMB_PTH"
        )
