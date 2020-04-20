class FakeIpGenerator:
    def __init__(self):
        self.fake_ip_parts = [1, 1, 1, 1]

    def generate_fake_ips_for_real_ips(self, real_ips):
        self.fake_ip_parts[2] += 1
        fake_ips = []
        for i in range(len(real_ips)):
            fake_ips.append('.'.join(str(part) for part in self.fake_ip_parts))
            self.fake_ip_parts[3] += 1
        return fake_ips
