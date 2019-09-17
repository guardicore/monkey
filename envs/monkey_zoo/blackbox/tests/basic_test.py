from time import sleep

from envs.monkey_zoo.blackbox.utils.test_timer import TestTimer
from envs.monkey_zoo.blackbox.log_handlers.test_logs_handler import TestLogsHandler

MAX_TIME_FOR_MONKEYS_TO_DIE = 5*60
WAIT_TIME_BETWEEN_REQUESTS = 10
TIME_FOR_MONKEY_PROCESS_TO_FINISH = 20


class BasicTest(object):

    def __init__(self, name, island_client, config_parser, analyzers, timeout):
        self.name = name
        self.island_client = island_client
        self.config_parser = config_parser
        self.analyzers = analyzers
        self.timeout = timeout

    def run(self):
        self.island_client.import_config(self.config_parser.config_raw)
        self.print_test_starting_info()
        try:
            self.island_client.run_monkey_local()
            self.test_until_timeout()
        finally:
            self.island_client.kill_all_monkeys()
            self.wait_until_monkeys_die()
            self.wait_for_monkey_process_to_finish()
            self.parse_logs()
            self.island_client.reset_env()

    def print_test_starting_info(self):
        print("Started {} test".format(self.name))
        print("Machines participating in test:")
        for target_ip in self.config_parser.get_ips_of_targets():
            print("  "+target_ip)
        print("")

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

    def parse_logs(self):
        print("\nParsing test logs:")
        TestLogsHandler(self.name, self.island_client).parse_test_logs()

    @staticmethod
    def wait_for_monkey_process_to_finish():
        sleep(TIME_FOR_MONKEY_PROCESS_TO_FINISH)
