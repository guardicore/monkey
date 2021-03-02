import logging
import os
from time import sleep

import pytest
from typing_extensions import Type

from envs.monkey_zoo.blackbox.analyzers.communication_analyzer import \
    CommunicationAnalyzer
from envs.monkey_zoo.blackbox.island_client.island_config_parser import \
    IslandConfigParser
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import \
    MonkeyIslandClient
from envs.monkey_zoo.blackbox.island_configs.config_template import ConfigTemplate
from envs.monkey_zoo.blackbox.island_configs.elastic import Elastic
from envs.monkey_zoo.blackbox.island_configs.hadoop import Hadoop
from envs.monkey_zoo.blackbox.island_configs.mssql import Mssql
from envs.monkey_zoo.blackbox.island_configs.performance import Performance
from envs.monkey_zoo.blackbox.island_configs.shellshock import ShellShock
from envs.monkey_zoo.blackbox.island_configs.smb_mimikatz import SmbMimikatz
from envs.monkey_zoo.blackbox.island_configs.smb_pth import SmbPth
from envs.monkey_zoo.blackbox.island_configs.ssh import Ssh
from envs.monkey_zoo.blackbox.island_configs.struts2 import Struts2
from envs.monkey_zoo.blackbox.island_configs.tunneling import Tunneling
from envs.monkey_zoo.blackbox.island_configs.weblogic import Weblogic
from envs.monkey_zoo.blackbox.island_configs.wmi_mimikatz import WmiMimikatz
from envs.monkey_zoo.blackbox.island_configs.wmi_pth import WmiPth
from envs.monkey_zoo.blackbox.log_handlers.test_logs_handler import \
    TestLogsHandler
from envs.monkey_zoo.blackbox.tests.exploitation import ExploitationTest
from envs.monkey_zoo.blackbox.tests.performance.map_generation import \
    MapGenerationTest
from envs.monkey_zoo.blackbox.tests.performance.map_generation_from_telemetries import \
    MapGenerationFromTelemetryTest
from envs.monkey_zoo.blackbox.tests.performance.report_generation import \
    ReportGenerationTest
from envs.monkey_zoo.blackbox.tests.performance.report_generation_from_telemetries import \
    ReportGenerationFromTelemetryTest
from envs.monkey_zoo.blackbox.tests.performance.telemetry_performance_test import \
    TelemetryPerformanceTest
from envs.monkey_zoo.blackbox.utils import gcp_machine_handlers

DEFAULT_TIMEOUT_SECONDS = 5*60
MACHINE_BOOTUP_WAIT_SECONDS = 30
GCP_TEST_MACHINE_LIST = ['sshkeys-11', 'sshkeys-12', 'elastic-4', 'elastic-5', 'hadoop-2', 'hadoop-3', 'mssql-16',
                         'mimikatz-14', 'mimikatz-15', 'struts2-23', 'struts2-24', 'tunneling-9', 'tunneling-10',
                         'tunneling-11', 'tunneling-12', 'weblogic-18', 'weblogic-19', 'shellshock-8', 'zerologon-25']
LOG_DIR_PATH = "./logs"
LOGGER = logging.getLogger(__name__)


@pytest.fixture(autouse=True, scope='session')
def GCPHandler(request, no_gcp):
    if not no_gcp:
        GCPHandler = gcp_machine_handlers.GCPHandler()
        GCPHandler.start_machines(" ".join(GCP_TEST_MACHINE_LIST))
        wait_machine_bootup()

        def fin():
            GCPHandler.stop_machines(" ".join(GCP_TEST_MACHINE_LIST))

        request.addfinalizer(fin)


@pytest.fixture(autouse=True, scope='session')
def delete_logs():
    LOGGER.info("Deleting monkey logs before new tests.")
    TestLogsHandler.delete_log_folder_contents(TestMonkeyBlackbox.get_log_dir_path())


def wait_machine_bootup():
    sleep(MACHINE_BOOTUP_WAIT_SECONDS)


@pytest.fixture(scope='class')
def island_client(island, quick_performance_tests):
    island_client_object = MonkeyIslandClient(island)
    if not quick_performance_tests:
        island_client_object.reset_env()
    yield island_client_object


@pytest.mark.usefixtures('island_client')
# noinspection PyUnresolvedReferences
class TestMonkeyBlackbox:

    @staticmethod
    def run_exploitation_test(island_client: MonkeyIslandClient,
                              config_template: Type[ConfigTemplate],
                              test_name: str,
                              timeout_in_seconds=DEFAULT_TIMEOUT_SECONDS):
        raw_config = IslandConfigParser.get_raw_config(config_template, island_client)
        analyzer = CommunicationAnalyzer(island_client,
                                         IslandConfigParser.get_ips_of_targets(raw_config))
        log_handler = TestLogsHandler(test_name, island_client, TestMonkeyBlackbox.get_log_dir_path())
        ExploitationTest(
            name=test_name,
            island_client=island_client,
            raw_config=raw_config,
            analyzers=[analyzer],
            timeout=timeout_in_seconds,
            log_handler=log_handler).run()

    @staticmethod
    def run_performance_test(performance_test_class, island_client,
                             config_template, timeout_in_seconds, break_on_timeout=False):
        raw_config = IslandConfigParser.get_raw_config(config_template, island_client)
        log_handler = TestLogsHandler(performance_test_class.TEST_NAME,
                                      island_client,
                                      TestMonkeyBlackbox.get_log_dir_path())
        analyzers = [CommunicationAnalyzer(island_client, IslandConfigParser.get_ips_of_targets(raw_config))]
        performance_test_class(island_client=island_client,
                               raw_config=raw_config,
                               analyzers=analyzers,
                               timeout=timeout_in_seconds,
                               log_handler=log_handler,
                               break_on_timeout=break_on_timeout).run()

    @staticmethod
    def get_log_dir_path():
        return os.path.abspath(LOG_DIR_PATH)

    def test_server_online(self, island_client):
        assert island_client.get_api_status() is not None

    def test_ssh_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, Ssh, "SSH_exploiter_and_keys")

    def test_hadoop_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, Hadoop, "Hadoop_exploiter", 6 * 60)

    def test_mssql_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, Mssql, "MSSQL_exploiter")

    def test_smb_and_mimikatz_exploiters(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, SmbMimikatz, "SMB_exploiter_mimikatz")

    def test_smb_pth(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, SmbPth, "SMB_PTH")

    def test_elastic_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, Elastic, "Elastic_exploiter")

    def test_struts_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, Struts2, "Strtuts2_exploiter")

    def test_weblogic_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, Weblogic, "Weblogic_exploiter")

    def test_shellshock_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, ShellShock, "Shellschock_exploiter")

    def test_tunneling(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, Tunneling, "Tunneling_exploiter", 15 * 60)

    def test_wmi_and_mimikatz_exploiters(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, WmiMimikatz, "WMI_exploiter,_mimikatz")

    def test_wmi_pth(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, WmiPth, "WMI_PTH")

    @pytest.mark.skip(reason="Perfomance test that creates env from fake telemetries is faster, use that instead.")
    def test_report_generation_performance(self, island_client, quick_performance_tests):
        """
        This test includes the SSH + Elastic + Hadoop + MSSQL machines all in one test
        for a total of 8 machines including the Monkey Island.

        Is has 2 analyzers - the regular one which checks all the Monkeys
        and the Timing one which checks how long the report took to execute
        """
        if not quick_performance_tests:
            TestMonkeyBlackbox.run_performance_test(ReportGenerationTest,
                                                    island_client,
                                                    Performance,
                                                    timeout_in_seconds=10*60)
        else:
            LOGGER.error("This test doesn't support 'quick_performance_tests' option.")
            assert False

    @pytest.mark.skip(reason="Perfomance test that creates env from fake telemetries is faster, use that instead.")
    def test_map_generation_performance(self, island_client, quick_performance_tests):
        if not quick_performance_tests:
            TestMonkeyBlackbox.run_performance_test(MapGenerationTest,
                                                    island_client,
                                                    "PERFORMANCE.conf",
                                                    timeout_in_seconds=10*60)
        else:
            LOGGER.error("This test doesn't support 'quick_performance_tests' option.")
            assert False

    def test_report_generation_from_fake_telemetries(self, island_client, quick_performance_tests):
        ReportGenerationFromTelemetryTest(island_client, quick_performance_tests).run()

    def test_map_generation_from_fake_telemetries(self, island_client, quick_performance_tests):
        MapGenerationFromTelemetryTest(island_client, quick_performance_tests).run()

    def test_telem_performance(self, island_client, quick_performance_tests):
        TelemetryPerformanceTest(island_client, quick_performance_tests).test_telemetry_performance()
