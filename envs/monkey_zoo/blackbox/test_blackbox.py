from time import sleep

import pytest

from envs.monkey_zoo.blackbox.utils.monkey_island_client import MonkeyIslandClient
from envs.monkey_zoo.blackbox.analyzers.communication_analyzer import CommunicationAnalyzer
from envs.monkey_zoo.blackbox.utils.island_config_parser import IslandConfigParser
from envs.monkey_zoo.blackbox.utils import gcp_machine_handlers
from envs.monkey_zoo.blackbox.tests.basic_test import BasicTest

DEFAULT_TIMEOUT_SECONDS = 4 * 60 # 4 minutes
DELAY_BETWEEN_TESTS = 10
GCP_TEST_MACHINE_LIST = ['sshkeys-11', 'sshkeys-12', 'elastic-4', 'elastic-5', 'haddop-2-v3', 'hadoop-3', 'mssql-16',
                         'mimikatz-14', 'mimikatz-15', 'final-test-struts2-23', 'final-test-struts2-24',
                         'tunneling-9', 'tunneling-10', 'tunneling-11', 'weblogic-18', 'weblogic-19', 'shellshock-8']


@pytest.fixture(autouse=True, scope='session')
def GCPHandler(request):
    GCPHandler = gcp_machine_handlers.GCPHandler()
    #GCPHandler.start_machines(" ".join(GCP_TEST_MACHINE_LIST))

    def fin():
        pass
        # GCPHandler.stop_machines(" ".join(GCP_TEST_MACHINE_LIST))

    request.addfinalizer(fin)


@pytest.fixture(scope='class')
def island_client(island):
    island_client_object = MonkeyIslandClient(island)
    yield island_client_object


@pytest.mark.usefixtures('island_client')
# noinspection PyUnresolvedReferences
class TestMonkeyBlackbox(object):

    def run_basic_test(self, island_client, conf_filename, test_name, timeout_in_seconds=DEFAULT_TIMEOUT_SECONDS):
        TestMonkeyBlackbox.wait_between_tests()
        config_parser = IslandConfigParser(conf_filename)
        analyzer = CommunicationAnalyzer(island_client, config_parser.get_ips_of_targets())
        BasicTest(test_name,
                  island_client,
                  config_parser.config_raw,
                  [analyzer],
                  timeout_in_seconds).run()

    @staticmethod
    def wait_between_tests():
        print("Waiting for ({:.0f} seconds) for old monkey's to die or GCP machines to boot up.".format(DELAY_BETWEEN_TESTS))
        sleep(DELAY_BETWEEN_TESTS)

    """
    def test_server_online(self, island_client):
        assert island_client.get_api_status() is not None

    def test_ssh_exploiter(self, island_client):
        self.run_basic_test(island_client, "SSH.conf", "SSH exploiter and keys")

    def test_hadoop_exploiter(self, island_client):
        self.run_basic_test(island_client, "HADOOP.conf", "Hadoop exploiter")

    def test_mssql_exploiter(self, island_client):
        self.run_basic_test(island_client, "MSSQL.conf", "MSSQL exploiter")
    """
    def test_smb_and_mimikatz_exploiters(self, island_client):
        self.run_basic_test(island_client, "SMB_MIMIKATZ.conf", "SMB exploiter, mimikatz")
    """
    def test_elastic_exploiter(self, island_client):
        self.run_basic_test(island_client, "ELASTIC.conf", "Elastic exploiter", 180)
    

    def test_struts_exploiter(self, island_client):
        self.run_basic_test(island_client, "STRUTS2.conf", "Strtuts2 exploiter")

    def test_weblogic_exploiter(self, island_client):
        self.run_basic_test(island_client, "WEBLOGIC.conf", "Weblogic exploiter")

    def test_shellshock_exploiter(self, island_client):
        self.run_basic_test(island_client, "SHELLSHOCK.conf", "Shellschock exploiter")

    def test_tunneling(self, island_client):
        self.run_basic_test(island_client, "TUNNELING.conf", "Tunneling exploiter")

    def test_wmi_exploiter(self, island_client):
        self.run_basic_test(island_client, "WMI_MIMIKATZ.conf", "WMI exploiter, mimikatz")
    """
