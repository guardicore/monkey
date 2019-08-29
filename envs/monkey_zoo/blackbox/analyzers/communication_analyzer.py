
class CommunicationAnalyzer(object):

    def __init__(self, island_client, machines):
        self.island_client = island_client
        self.machines = machines

    def analyze_test_results(self):
        for machine in self.machines:
            if self.did_monkey_communicate_back(machine):
                print("Monkey from {} communicated back".format(machine))

    def did_monkey_communicate_back(self, monkey_ip):
        request = self.island_client.send_get_request("api/telemetry", {'telem_category': 'state'})


