from infection_monkey.model.host import VictimHost


class VictimHostGenerator(object):
    def __init__(self, network_ranges, blocked_ips, same_machine_ips):
        self.blocked_ips = blocked_ips
        self.ranges = network_ranges
        self.local_addresses = same_machine_ips

    def generate_victims(self, chunk_size):
        """
        Generates VictimHosts in chunks from all the instances network ranges
        :param chunk_size: Maximum size of each chunk
        """
        chunk = []
        for net_range in self.ranges:
            for victim in self.generate_victims_from_range(net_range):
                chunk.append(victim)
                if len(chunk) == chunk_size:
                    yield chunk
                    chunk = []
        if chunk:  # finished with number of victims < chunk_size
            yield chunk

    def generate_victims_from_range(self, net_range):
        """
        Generates VictimHosts from a given netrange
        :param net_range: Network range object
        :return: Generator of VictimHost objects
        """
        for address in net_range:
            if not self.is_ip_scannable(address):  # check if the IP should be skipped
                continue
            if hasattr(net_range, 'domain_name'):
                victim = VictimHost(address, net_range.domain_name)
            else:
                victim = VictimHost(address)
            yield victim

    def is_ip_scannable(self, ip_address):
        if ip_address in self.local_addresses:
            return False
        if ip_address in self.blocked_ips:
            return False
        return True
