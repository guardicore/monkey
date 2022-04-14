import logging
import os
from time import sleep

import pytest
from typing_extensions import Type

from envs.monkey_zoo.blackbox.analyzers.communication_analyzer import CommunicationAnalyzer
from envs.monkey_zoo.blackbox.analyzers.zerologon_analyzer import ZerologonAnalyzer
from envs.monkey_zoo.blackbox.config_templates.config_template import ConfigTemplate
from envs.monkey_zoo.blackbox.config_templates.single_tests.hadoop import Hadoop
from envs.monkey_zoo.blackbox.config_templates.single_tests.log4j_logstash import Log4jLogstash
from envs.monkey_zoo.blackbox.config_templates.single_tests.log4j_solr import Log4jSolr
from envs.monkey_zoo.blackbox.config_templates.single_tests.log4j_tomcat import Log4jTomcat
from envs.monkey_zoo.blackbox.config_templates.single_tests.mssql import Mssql
from envs.monkey_zoo.blackbox.config_templates.single_tests.performance import Performance
from envs.monkey_zoo.blackbox.config_templates.single_tests.powershell import PowerShell
from envs.monkey_zoo.blackbox.config_templates.single_tests.powershell_credentials_reuse import (
    PowerShellCredentialsReuse,
)
from envs.monkey_zoo.blackbox.config_templates.single_tests.smb_mimikatz import SmbMimikatz
from envs.monkey_zoo.blackbox.config_templates.single_tests.smb_pth import SmbPth
from envs.monkey_zoo.blackbox.config_templates.single_tests.ssh import Ssh
from envs.monkey_zoo.blackbox.config_templates.single_tests.tunneling import Tunneling
from envs.monkey_zoo.blackbox.config_templates.single_tests.wmi_mimikatz import WmiMimikatz
from envs.monkey_zoo.blackbox.config_templates.single_tests.wmi_pth import WmiPth
from envs.monkey_zoo.blackbox.config_templates.single_tests.zerologon import Zerologon
from envs.monkey_zoo.blackbox.gcp_test_machine_list import GCP_TEST_MACHINE_LIST
from envs.monkey_zoo.blackbox.island_client.island_config_parser import IslandConfigParser
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient
from envs.monkey_zoo.blackbox.log_handlers.test_logs_handler import TestLogsHandler
from envs.monkey_zoo.blackbox.tests.exploitation import ExploitationTest
from envs.monkey_zoo.blackbox.tests.performance.map_generation import MapGenerationTest
from envs.monkey_zoo.blackbox.tests.performance.map_generation_from_telemetries import (
    MapGenerationFromTelemetryTest,
)
from envs.monkey_zoo.blackbox.tests.performance.report_generation import ReportGenerationTest
from envs.monkey_zoo.blackbox.tests.performance.report_generation_from_telemetries import (
    ReportGenerationFromTelemetryTest,
)
from envs.monkey_zoo.blackbox.tests.performance.telemetry_performance_test import (
    TelemetryPerformanceTest,
)
from envs.monkey_zoo.blackbox.utils.gcp_machine_handlers import (
    initialize_gcp_client,
    start_machines,
    stop_machines,
)
from monkey_island.cc.services.mode.mode_enum import IslandModeEnum

DEFAULT_TIMEOUT_SECONDS = 2 * 60
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
    def run_performance_test(
        performance_test_class,
        island_client,
        config_template,
        timeout_in_seconds,
        break_on_timeout=False,
    ):
        raw_config = IslandConfigParser.get_raw_config(config_template, island_client)
        log_handler = TestLogsHandler(
            performance_test_class.TEST_NAME, island_client, TestMonkeyBlackbox.get_log_dir_path()
        )
        analyzers = [
            CommunicationAnalyzer(island_client, IslandConfigParser.get_ips_of_targets(raw_config))
        ]
        performance_test_class(
            island_client=island_client,
            raw_config=raw_config,
            analyzers=analyzers,
            timeout=timeout_in_seconds,
            log_handler=log_handler,
            break_on_timeout=break_on_timeout,
        ).run()

    @staticmethod
    def get_log_dir_path():
        return os.path.abspath(LOG_DIR_PATH)

    def test_ssh_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, Ssh, "SSH_exploiter_and_keys")

    def test_hadoop_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, Hadoop, "Hadoop_exploiter", 6 * 60)

    def test_mssql_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, Mssql, "MSSQL_exploiter")

    def test_powershell_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, PowerShell, "PowerShell_Remoting_exploiter"
        )

    @pytest.mark.skip_powershell_reuse
    def test_powershell_exploiter_credentials_reuse(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client,
            PowerShellCredentialsReuse,
            "PowerShell_Remoting_exploiter_credentials_reuse",
        )

    def test_smb_and_mimikatz_exploiters(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, SmbMimikatz, "SMB_exploiter_mimikatz"
        )

    def test_smb_pth(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, SmbPth, "SMB_PTH")

    def test_log4j_solr_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, Log4jSolr, "Log4Shell_Solr_exploiter"
        )

    def test_log4j_tomcat_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, Log4jTomcat, "Log4Shell_tomcat_exploiter"
        )

    def test_log4j_logstash_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, Log4jLogstash, "Log4Shell_logstash_exploiter"
        )

    def test_tunneling(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, Tunneling, "Tunneling_exploiter", 3 * 60
        )

    def test_wmi_and_mimikatz_exploiters(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(
            island_client, WmiMimikatz, "WMI_exploiter,_mimikatz"
        )

    def test_wmi_pth(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, WmiPth, "WMI_PTH")

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
            timeout=DEFAULT_TIMEOUT_SECONDS,
            log_handler=log_handler,
        ).run()

    @pytest.mark.skip(
        reason="Perfomance test that creates env from fake telemetries is faster, use that instead."
    )
    def test_report_generation_performance(self, island_client, quick_performance_tests):
        """
        This test includes the SSH + Hadoop + MSSQL machines all in one test
        for a total of 8 machines including the Monkey Island.

        Is has 2 analyzers - the regular one which checks all the Monkeys
        and the Timing one which checks how long the report took to execute
        """
        if not quick_performance_tests:
            TestMonkeyBlackbox.run_performance_test(
                ReportGenerationTest, island_client, Performance, timeout_in_seconds=10 * 60
            )
        else:
            LOGGER.error("This test doesn't support 'quick_performance_tests' option.")
            assert False

    @pytest.mark.skip(
        reason="Perfomance test that creates env from fake telemetries is faster, use that instead."
    )
    def test_map_generation_performance(self, island_client, quick_performance_tests):
        if not quick_performance_tests:
            TestMonkeyBlackbox.run_performance_test(
                MapGenerationTest, island_client, "PERFORMANCE.conf", timeout_in_seconds=10 * 60
            )
        else:
            LOGGER.error("This test doesn't support 'quick_performance_tests' option.")
            assert False

    @pytest.mark.run_performance_tests
    def test_report_generation_from_fake_telemetries(self, island_client, quick_performance_tests):
        ReportGenerationFromTelemetryTest(island_client, quick_performance_tests).run()

    @pytest.mark.run_performance_tests
    def test_map_generation_from_fake_telemetries(self, island_client, quick_performance_tests):
        MapGenerationFromTelemetryTest(island_client, quick_performance_tests).run()

    @pytest.mark.run_performance_tests
    def test_telem_performance(self, island_client, quick_performance_tests):
        TelemetryPerformanceTest(
            island_client, quick_performance_tests
        ).test_telemetry_performance()
