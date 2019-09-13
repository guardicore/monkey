LOG_INIT_MESSAGE = "Analysis didn't run."


class CommunicationAnalyzer(object):

    def __init__(self, island_client, machine_ips):
        self.island_client = island_client
        self.machine_ips = machine_ips
        self.log = AnalyzerLog(self.__class__.__name__)

    def analyze_test_results(self):
        self.log.clear()
        for machine_ip in self.machine_ips:
            if not self.did_monkey_communicate_back(machine_ip):
                self.log.add_entry("Monkey from {} didn't communicate back".format(machine_ip))
                return False
            self.log.add_entry("Monkey from {} communicated back".format(machine_ip))
        return True

    def did_monkey_communicate_back(self, machine_ip):
        query = {'ip_addresses': {'$elemMatch': {'$eq': machine_ip}}}
        return len(self.island_client.find_monkeys_in_db(query)) > 0


class AnalyzerLog(object):

    def __init__(self, analyzer_name):
        self.contents = LOG_INIT_MESSAGE
        self.name = analyzer_name

    def clear(self):
        self.contents = ""

    def add_entry(self, message):
        self.contents = "{}\n{}".format(self.contents, message)

    def get_contents(self):
        return "{}: {}\n".format(self.name, self.contents)
