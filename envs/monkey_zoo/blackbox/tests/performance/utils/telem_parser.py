from typing import List, Dict
from os import listdir, path
import copy
import random
import json


TELEM_DIR_PATH = './tests/performance/test_telems'


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


class Monkey:
    def __init__(self, ips, guid, fake_ip_generator: FakeIpGenerator, on_island=False):
        self.ips = ips
        self.guid = guid
        self.fake_ip_generator = fake_ip_generator
        self.on_island = on_island
        self.fake_guid = str(random.randint(1000000000000, 9999999999999))
        self.fake_ips = fake_ip_generator.generate_fake_ips_for_real_ips(ips)

    def change_fake_data(self):
        self.fake_ips = self.fake_ip_generator.generate_fake_ips_for_real_ips(self.ips)
        self.fake_guid = str(random.randint(1000000000000, 9999999999999))


class TelemParser:
    def __init__(self, island_ip: str, multiplier: int):
        self.multiplier = multiplier
        self.fake_ip_generator = FakeIpGenerator()
        self.island_ip = island_ip

    def multiply_telems(self):
        telems = TelemParser.get_all_telemetries()
        telem_contents = [json.loads(telem['content']) for telem in telems]
        monkeys = self.get_monkeys_from_telems(telem_contents)
        for i in range(self.multiplier):
            for monkey in monkeys:
                monkey.change_fake_data()
            fake_telem_batch = copy.deepcopy(telems)
            TelemParser.fabricate_monkeys_in_telems(fake_telem_batch, monkeys)
            TelemParser.offset_telem_times(iteration=i, telems=fake_telem_batch)
            TelemParser.save_teletries_to_files(fake_telem_batch)

    @staticmethod
    def fabricate_monkeys_in_telems(telems: List[Dict], monkeys: List[Monkey]):
        for telem in telems:
            for monkey in monkeys:
                if monkey.on_island:
                    continue
                if (monkey.guid in telem['content'] or monkey.guid in telem['endpoint']) and not monkey.on_island:
                    telem['content'] = telem['content'].replace(monkey.guid, monkey.fake_guid)
                    telem['endpoint'] = telem['endpoint'].replace(monkey.guid, monkey.fake_guid)
                for i in range(len(monkey.ips)):
                    telem['content'] = telem['content'].replace(monkey.ips[i], monkey.fake_ips[i])

    @staticmethod
    def offset_telem_times(iteration: int, telems: List[Dict]):
        for telem in telems:
            telem['time']['$date'] += iteration * 1000

    @staticmethod
    def save_teletries_to_files(telems: List[Dict]):
        for telem in telems:
            TelemParser.save_telemetry_to_file(telem)

    @staticmethod
    def save_telemetry_to_file(telem):
        telem_filename = telem['name'] + telem['method']
        for i in range(10000):
            if not path.exists(path.join(TELEM_DIR_PATH, (str(i) + telem_filename))):
                telem_filename = str(i) + telem_filename
                break
        with open(path.join(TELEM_DIR_PATH, telem_filename), 'w') as file:
            file.write(json.dumps(telem))

    @staticmethod
    def read_telem_files() -> List[str]:
        telems = []
        file_paths = [path.join(TELEM_DIR_PATH, f) for f in listdir(TELEM_DIR_PATH)
                      if path.isfile(path.join(TELEM_DIR_PATH, f))]
        for file_path in file_paths:
            with open(file_path, 'r') as telem_file:
                telems.append(telem_file.readline())
        return telems

    @staticmethod
    def get_all_telemetries():
        return [json.loads(t) for t in TelemParser.read_telem_files()]

    def get_monkeys_from_telems(self, telems: List[Dict]):
        monkeys = []
        for telem in [telem for telem in telems if 'telem_category' in telem and telem['telem_category'] == 'system_info']:
            if 'network_info' not in telem['data']:
                continue
            guid = telem['monkey_guid']
            monkey_present = [monkey for monkey in monkeys if monkey.guid == guid]
            if not monkey_present:
                ips = [net_info['addr'] for net_info in telem['data']['network_info']['networks']]
                if self.island_ip in ips:
                    on_island = True
                else:
                    on_island = False

                monkeys.append(Monkey(ips=ips,
                                      guid=guid,
                                      fake_ip_generator=self.fake_ip_generator,
                                      on_island=on_island))
        return monkeys


if __name__ == "__main__":
    TelemParser(island_ip='192.168.56.1', multiplier=100).multiply_telems()
