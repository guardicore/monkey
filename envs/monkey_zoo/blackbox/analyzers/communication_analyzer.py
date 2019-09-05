import json


class CommunicationAnalyzer(object):

    def __init__(self, island_client, machine_ips):
        self.island_client = island_client
        self.machine_ips = machine_ips

    def analyze_test_results(self):
        for machine_ip in self.machine_ips:
            if not self.did_monkey_communicate_back(machine_ip):
                return False
            print("Monkey from {} communicated back".format(machine_ip))
        return True

    def did_monkey_communicate_back(self, machine_ip):
        query = json.dumps({'ip_addresses': {'$elemMatch': {'$eq': machine_ip}}})
        response = self.island_client.send_get_request("api/test/monkey", {'find_query': query})
        return len(json.loads(response.content)['results']) > 0


