import random

from envs.monkey_zoo.blackbox.tests.performance.telem_sample_parsing.sample_multiplier.fake_ip_generator import \
    FakeIpGenerator


class FakeMonkey:
    def __init__(self, ips, guid, fake_ip_generator: FakeIpGenerator, on_island=False):
        self.original_ips = ips
        self.original_guid = guid
        self.fake_ip_generator = fake_ip_generator
        self.on_island = on_island
        self.fake_guid = str(random.randint(1000000000000, 9999999999999))  # noqa: DUO102
        self.fake_ips = fake_ip_generator.generate_fake_ips_for_real_ips(ips)

    def change_fake_data(self):
        self.fake_ips = self.fake_ip_generator.generate_fake_ips_for_real_ips(self.original_ips)
        self.fake_guid = str(random.randint(1000000000000, 9999999999999))  # noqa: DUO102
