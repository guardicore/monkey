from unittest import TestCase

from common.network.network_range import CidrRange, SingleIpRange
from infection_monkey.model.victim_host_generator import VictimHostGenerator


class VictimHostGeneratorTester(TestCase):

    def setUp(self):
        self.cidr_range = CidrRange("10.0.0.0/28", False)  # this gives us 15 hosts
        self.local_host_range = SingleIpRange('localhost')
        self.random_single_ip_range = SingleIpRange('41.50.13.37')

    def test_chunking(self):
        chunk_size = 3
        # current test setup is 15+1+1-1 hosts
        test_ranges = [self.cidr_range, self.local_host_range, self.random_single_ip_range]
        generator = VictimHostGenerator(test_ranges, '10.0.0.1', [])
        victims = generator.generate_victims(chunk_size)
        for i in range(5):  # quickly check the equally sided chunks
            self.assertEqual(len(next(victims)), chunk_size)
        victim_chunk_last = next(victims)
        self.assertEqual(len(victim_chunk_last), 1)

    def test_remove_blocked_ip(self):
        generator = VictimHostGenerator(self.cidr_range, ['10.0.0.1'], [])

        victims = list(generator.generate_victims_from_range(self.cidr_range))
        self.assertEqual(len(victims), 14)  # 15 minus the 1 we blocked

    def test_remove_local_ips(self):
        generator = VictimHostGenerator([], [], [])
        generator.local_addresses = ['127.0.0.1']
        victims = list(generator.generate_victims_from_range(self.local_host_range))
        self.assertEqual(len(victims), 0)  # block the local IP

    def test_generate_domain_victim(self):
        # domain name victim
        generator = VictimHostGenerator([], [], [])  # dummy object
        victims = list(generator.generate_victims_from_range(self.local_host_range))
        self.assertEqual(len(victims), 1)
        self.assertEqual(victims[0].domain_name, 'localhost')

        # don't generate for other victims
        victims = list(generator.generate_victims_from_range(self.random_single_ip_range))
        self.assertEqual(len(victims), 1)
        self.assertEqual(victims[0].domain_name, '')
