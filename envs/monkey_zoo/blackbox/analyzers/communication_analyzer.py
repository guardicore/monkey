from envs.monkey_zoo.blackbox.analyzers.analyzer import Analyzer
from envs.monkey_zoo.blackbox.analyzers.analyzer_log import AnalyzerLog


class CommunicationAnalyzer(Analyzer):

    def __init__(self, island_client, machine_ips):
        self.island_client = island_client
        self.machine_ips = machine_ips
        self.log = AnalyzerLog(self.__class__.__name__)

    def analyze_test_results(self):
        self.log.clear()
        all_monkeys_communicated = True
        for machine_ip in self.machine_ips:
            if not self.did_monkey_communicate_back(machine_ip):
                self.log.add_entry("Monkey from {} didn't communicate back".format(machine_ip))
                all_monkeys_communicated = False
            else:
                self.log.add_entry("Monkey from {} communicated back".format(machine_ip))
        return all_monkeys_communicated

    def did_monkey_communicate_back(self, machine_ip):
        query = {'ip_addresses': {'$elemMatch': {'$eq': machine_ip}}}
        return len(self.island_client.find_monkeys_in_db(query)) > 0
