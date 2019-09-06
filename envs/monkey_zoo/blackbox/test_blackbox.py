import unittest
from time import sleep, time

import pytest

from envs.monkey_zoo.blackbox.monkey_island_client import MonkeyIslandClient
from envs.monkey_zoo.blackbox.analyzers.communication_analyzer import CommunicationAnalyzer
from envs.monkey_zoo.blackbox.island_config_parser import IslandConfigParser
from envs.monkey_zoo.blackbox.gcp_machine_handlers import GCPHandler


MACHINE_BOOT_TIME_SECONDS = 20
TEST_TIME_SECONDS = 70
DELAY_BETWEEN_TESTS = 1


class BlackBoxTest(object):

    def __init__(self, name, island_client, island_config, analyzers, timeout=TEST_TIME_SECONDS):
        self.name = name
        self.island_client = island_client
        self.island_config = island_config
        self.analyzers = analyzers
        self.timeout = timeout

    def run(self):
        self.island_client.import_config(self.island_config)
        self.island_client.run_monkey_local()
        self.test_until_timeout()
        self.island_client.reset_env()

    def test_until_timeout(self):
        timer = TestTimer(self.timeout)
        while not timer.timed_out():
            if self.analyzers_pass():
                self.log_success(timer)
                return
            sleep(DELAY_BETWEEN_TESTS)
        self.log_failure(timer)
        assert False

    def log_success(self, timer):
        print(self.get_analyzer_logs())
        print("{} test passed, time taken: {:.1f} seconds.".format(self.name, timer.get_time_taken()))

    def log_failure(self, timer):
        print(self.get_analyzer_logs())
        print("{} test failed because of timeout. Time taken: {:.1f} seconds.".format(self.name,
                                                                                      timer.get_time_taken()))

    def analyzers_pass(self):
        for analyzer in self.analyzers:
            if not analyzer.analyze_test_results():
                return False
        return True

    def get_analyzer_logs(self):
        log = ""
        for analyzer in self.analyzers:
            log += "\n"+analyzer.log.get_contents()
        return log


class TestTimer(object):
    def __init__(self, timeout):
        self.timeout_time = TestTimer.get_timeout_time(timeout)
        self.start_time = time()

    def timed_out(self):
        return time() > self.timeout_time

    def get_time_taken(self):
        return time() - self.start_time

    @staticmethod
    def get_timeout_time(timeout):
        return time() + timeout


@pytest.mark.usefixtures("island")
# noinspection PyUnresolvedReferences
class TestMonkeyBlackbox(unittest.TestCase):

    def setUp(self):
        self.GCPHandler = GCPHandler()
        self.island_client = MonkeyIslandClient(self.island)
        self.GCPHandler.start_machines("sshkeys-11 sshkeys-12")
        TestMonkeyBlackbox.wait_for_machine_boot()

    def tearDown(self):
        self.GCPHandler.stop_machines("sshkeys-11 sshkeys-12")
        print("Killing all GCP machines...")

    def test_server_online(self):
        assert self.island_client.get_api_status() is not None

    def test_ssh_exec(self):
        conf_file_name = 'SSH.conf'
        config_parser = IslandConfigParser(conf_file_name)
        analyzer = CommunicationAnalyzer(self.island_client, config_parser.get_ips_of_targets())
        BlackBoxTest("SSH test", self.island_client, config_parser.config_raw, [analyzer]).run()

    @staticmethod
    def wait_for_machine_boot(time=MACHINE_BOOT_TIME_SECONDS):
        print("Waiting for machines to fully boot up({:.0f} seconds).".format(time))
        sleep(time)
