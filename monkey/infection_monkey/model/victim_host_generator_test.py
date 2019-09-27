from unittest import TestCase
from infection_monkey.model.victim_host_generator import VictimHostGenerator
from common.network.network_range import CidrRange, SingleIpRange


class VictimHostGeneratorTester(TestCase):

    def setUp(self):
        self.test_ranges = [CidrRange("10.0.0.0/28", False),  # this gives us 15 hosts
                            SingleIpRange('41.50.13.37'),
                            SingleIpRange('localhost')
                            ]
        self.generator = VictimHostGenerator(self.test_ranges, '10.0.0.1')
        self.generator._ip_addresses = []  # test later on

    def test_chunking(self):
        chunk_size = 3
        # current test setup is 15+1+1-1 hosts
        victims = self.generator.generate_victims(chunk_size)
        for i in range(5):  # quickly check the equally sided chunks
            self.assertEqual(len(victims.next()), chunk_size)
        victim_chunk_last = victims.next()
        self.assertEqual(len(victim_chunk_last), 1)

    def test_remove_blocked_ip(self):
        victims = list(self.generator.generate_victims_from_range(self.test_ranges[0]))
        self.assertEqual(len(victims), 14)  # 15 minus the 1 we blocked

    def test_remove_local_ips(self):
        self.generator._ip_addresses = ['127.0.0.1']
        victims = list(self.generator.generate_victims_from_range(self.test_ranges[-1]))
        self.assertEqual(len(victims), 0)  # block the local IP

    def test_generate_domain_victim(self):
        # domain name victim
        self.generator._ip_addresses = []
        victims = list(self.generator.generate_victims_from_range(self.test_ranges[-1]))
        self.assertEqual(len(victims), 1)
        self.assertEqual(victims[0].domain_name, 'localhost')

        # don't generate for other victims
        victims = list(self.generator.generate_victims_from_range(self.test_ranges[1]))
        self.assertEqual(len(victims), 1)
        self.assertEqual(victims[0].domain_name, '')
