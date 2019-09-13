from time import sleep

from envs.monkey_zoo.blackbox.utils.test_timer import TestTimer
from envs.monkey_zoo.blackbox.log_handlers.test_logs import TestLogsHandler

MAX_TIME_FOR_MONKEYS_TO_DIE = 5*60
WAIT_TIME_BETWEEN_REQUESTS = 10


class BasicTest(object):

    def __init__(self, name, island_client, island_config, analyzers, timeout):
        self.name = name
        self.island_client = island_client
        self.island_config = island_config
        self.analyzers = analyzers
        self.timeout = timeout

    def run(self):
        self.island_client.import_config(self.island_config)
        try:
            self.island_client.run_monkey_local()
            self.test_until_timeout()
        except AssertionError:
            print("Test {} failed. Downloading logs of all monkeys.".format(self.name))
            TestLogsHandler(self.name, self.island_client).download_logs()
            raise
        finally:
            self.island_client.kill_all_monkeys()
            self.wait_until_monkeys_die()
            self.island_client.reset_env()

    def test_until_timeout(self):
        timer = TestTimer(self.timeout)
        while not timer.timed_out():
            if self.all_analyzers_pass():
                self.log_success(timer)
                return
        self.log_failure(timer)
        assert False

    def log_success(self, timer):
        print(self.get_analyzer_logs())
        print("{} test passed, time taken: {:.1f} seconds.".format(self.name, timer.get_time_taken()))

    def log_failure(self, timer):
        print(self.get_analyzer_logs())
        print("{} test failed because of timeout. Time taken: {:.1f} seconds.".format(self.name,
                                                                                      timer.get_time_taken()))

    def all_analyzers_pass(self):
        for analyzer in self.analyzers:
            if not analyzer.analyze_test_results():
                return False
        return True

    def get_analyzer_logs(self):
        log = ""
        for analyzer in self.analyzers:
            log += "\n"+analyzer.log.get_contents()
        return log

    def wait_until_monkeys_die(self):
        time_passed = 0
        while not self.island_client.is_all_monkeys_dead() and time_passed < MAX_TIME_FOR_MONKEYS_TO_DIE:
            sleep(WAIT_TIME_BETWEEN_REQUESTS)
            time_passed += WAIT_TIME_BETWEEN_REQUESTS
        if time_passed > MAX_TIME_FOR_MONKEYS_TO_DIE:
            print("Some monkeys didn't die after the test, passing")
            assert False
