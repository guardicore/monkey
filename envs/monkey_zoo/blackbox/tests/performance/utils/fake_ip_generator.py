from typing import List


class FakeIpGenerator:
    def __init__(self):
        self.fake_ip_parts = [1, 1, 1, 1]

    def generate_fake_ips_for_real_ips(self, real_ips: List[str]) -> List[str]:
        fake_ips = []
        for i in range(len(real_ips)):
            fake_ips.append('.'.join(str(part) for part in self.fake_ip_parts))
            self.increment_ip()
        return fake_ips

    def increment_ip(self):
        self.fake_ip_parts[3] += 1
        self.try_fix_ip_range()

    def try_fix_ip_range(self):
        for i in range(len(self.fake_ip_parts)):
            if self.fake_ip_parts[i] > 256:
                if i-1 < 0:
                    raise Exception("Fake IP's out of range.")
                self.fake_ip_parts[i-1] += 1
                self.fake_ip_parts[i] = 1
