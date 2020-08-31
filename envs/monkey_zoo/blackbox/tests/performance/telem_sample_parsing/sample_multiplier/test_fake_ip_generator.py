from unittest import TestCase

from envs.monkey_zoo.blackbox.tests.performance.telem_sample_parsing.sample_multiplier.fake_ip_generator import \
    FakeIpGenerator


class TestFakeIpGenerator(TestCase):

    def test_fake_ip_generation(self):
        fake_ip_gen = FakeIpGenerator()
        self.assertListEqual([1, 1, 1, 1], fake_ip_gen.fake_ip_parts)
        for i in range(256):
            fake_ip_gen.generate_fake_ips_for_real_ips(['1.1.1.1'])
        self.assertListEqual(['1.1.2.1'], fake_ip_gen.generate_fake_ips_for_real_ips(['1.1.1.1']))
        fake_ip_gen.fake_ip_parts = [256, 256, 255, 256]
        self.assertListEqual(['256.256.255.256', '256.256.256.1'],
                             fake_ip_gen.generate_fake_ips_for_real_ips(['1.1.1.1', '1.1.1.2']))
        fake_ip_gen.fake_ip_parts = [256, 256, 256, 256]
        self.assertRaises(Exception, fake_ip_gen.generate_fake_ips_for_real_ips(['1.1.1.1']))
