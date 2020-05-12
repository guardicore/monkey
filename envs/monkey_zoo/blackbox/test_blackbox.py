import os
import logging

import pytest
from time import sleep

from envs.monkey_zoo.blackbox.analyzers.communication_analyzer import CommunicationAnalyzer
from envs.monkey_zoo.blackbox.island_client.island_config_parser import IslandConfigParser
from envs.monkey_zoo.blackbox.island_client.monkey_island_client import MonkeyIslandClient
from envs.monkey_zoo.blackbox.log_handlers.test_logs_handler import TestLogsHandler
from envs.monkey_zoo.blackbox.tests.exploitation import ExploitationTest
from envs.monkey_zoo.blackbox.tests.performance.map_generation import MapGenerationTest
from envs.monkey_zoo.blackbox.tests.performance.map_generation_from_telemetries import MapGenerationFromTelemetryTest
from envs.monkey_zoo.blackbox.tests.performance.report_generation import ReportGenerationTest
from envs.monkey_zoo.blackbox.tests.performance.report_generation_from_telemetries import \
    ReportGenerationFromTelemetryTest
from envs.monkey_zoo.blackbox.tests.performance.telemetry_performance_test import TelemetryPerformanceTest
from envs.monkey_zoo.blackbox.utils import gcp_machine_handlers

DEFAULT_TIMEOUT_SECONDS = 5*60
MACHINE_BOOTUP_WAIT_SECONDS = 30
GCP_TEST_MACHINE_LIST = ['sshkeys-11', 'sshkeys-12', 'elastic-4', 'elastic-5', 'hadoop-2', 'hadoop-3', 'mssql-16',
                         'mimikatz-14', 'mimikatz-15', 'struts2-23', 'struts2-24', 'tunneling-9', 'tunneling-10',
                         'tunneling-11', 'tunneling-12', 'weblogic-18', 'weblogic-19', 'shellshock-8']
LOG_DIR_PATH = "./logs"
LOGGER = logging.getLogger(__name__)


@pytest.fixture(autouse=True, scope='session')
def GCPHandler(request):
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
def island_client(island):
    island_client_object = MonkeyIslandClient(island)
    island_client_object.reset_env()
    yield island_client_object


@pytest.mark.usefixtures('island_client')
# noinspection PyUnresolvedReferences
class TestMonkeyBlackbox(object):

    @staticmethod
    def run_exploitation_test(island_client, conf_filename, test_name, timeout_in_seconds=DEFAULT_TIMEOUT_SECONDS):
        config_parser = IslandConfigParser(conf_filename)
        analyzer = CommunicationAnalyzer(island_client, config_parser.get_ips_of_targets())
        log_handler = TestLogsHandler(test_name, island_client, TestMonkeyBlackbox.get_log_dir_path())
        ExploitationTest(
            name=test_name,
            island_client=island_client,
            config_parser=config_parser,
            analyzers=[analyzer],
            timeout=timeout_in_seconds,
            log_handler=log_handler).run()

    @staticmethod
    def run_performance_test(performance_test_class, island_client,
                             conf_filename, timeout_in_seconds, break_on_timeout=False):
        config_parser = IslandConfigParser(conf_filename)
        log_handler = TestLogsHandler(performance_test_class.TEST_NAME,
                                      island_client,
                                      TestMonkeyBlackbox.get_log_dir_path())
        analyzers = [CommunicationAnalyzer(island_client, config_parser.get_ips_of_targets())]
        performance_test_class(island_client=island_client,
                               config_parser=config_parser,
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
        TestMonkeyBlackbox.run_exploitation_test(island_client, "SSH.conf", "SSH_exploiter_and_keys")

    def test_hadoop_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, "HADOOP.conf", "Hadoop_exploiter", 6 * 60)

    def test_mssql_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, "MSSQL.conf", "MSSQL_exploiter")

    def test_smb_and_mimikatz_exploiters(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, "SMB_MIMIKATZ.conf", "SMB_exploiter_mimikatz")

    def test_smb_pth(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, "SMB_PTH.conf", "SMB_PTH")

    def test_elastic_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, "ELASTIC.conf", "Elastic_exploiter")

    def test_struts_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, "STRUTS2.conf", "Strtuts2_exploiter")

    def test_weblogic_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, "WEBLOGIC.conf", "Weblogic_exploiter")

    def test_shellshock_exploiter(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, "SHELLSHOCK.conf", "Shellschock_exploiter")

    def test_tunneling(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, "TUNNELING.conf", "Tunneling_exploiter", 15 * 60)

    def test_wmi_and_mimikatz_exploiters(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, "WMI_MIMIKATZ.conf", "WMI_exploiter,_mimikatz")

    def test_wmi_pth(self, island_client):
        TestMonkeyBlackbox.run_exploitation_test(island_client, "WMI_PTH.conf", "WMI_PTH")

    def test_report_generation_performance(self, island_client):
        """
        This test includes the SSH + Elastic + Hadoop + MSSQL machines all in one test
        for a total of 8 machines including the Monkey Island.

        Is has 2 analyzers - the regular one which checks all the Monkeys
        and the Timing one which checks how long the report took to execute
        """
        TestMonkeyBlackbox.run_performance_test(ReportGenerationTest,
                                                island_client,
                                                "PERFORMANCE.conf",
                                                timeout_in_seconds=10*60)

    def test_map_generation_performance(self, island_client):
        TestMonkeyBlackbox.run_performance_test(MapGenerationTest,
                                                island_client,
                                                "PERFORMANCE.conf",
                                                timeout_in_seconds=10*60)

    def test_report_generation_from_fake_telemetries(self, island_client):
        ReportGenerationFromTelemetryTest(island_client).run()

    def test_map_generation_from_fake_telemetries(self, island_client):
        MapGenerationFromTelemetryTest(island_client).run()

    def test_telem_performance(self, island_client):
        TelemetryPerformanceTest(island_client).test_telemetry_performance()
