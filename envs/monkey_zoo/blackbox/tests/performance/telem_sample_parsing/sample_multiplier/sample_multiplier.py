import copy
import json
import logging
import sys
from typing import Dict, List

from tqdm import tqdm

from envs.monkey_zoo.blackbox.tests.performance.telem_sample_parsing.sample_file_parser import \
    SampleFileParser
from envs.monkey_zoo.blackbox.tests.performance.telem_sample_parsing.sample_multiplier.fake_ip_generator import \
    FakeIpGenerator
from envs.monkey_zoo.blackbox.tests.performance.telem_sample_parsing.sample_multiplier.fake_monkey import \
    FakeMonkey

TELEM_DIR_PATH = './tests/performance/telemetry_sample'
LOGGER = logging.getLogger(__name__)


class SampleMultiplier:

    def __init__(self, multiplier: int):
        self.multiplier = multiplier
        self.fake_ip_generator = FakeIpGenerator()

    def multiply_telems(self):
        telems = SampleFileParser.get_all_telemetries()
        telem_contents = [json.loads(telem['content']) for telem in telems]
        monkeys = self.get_monkeys_from_telems(telem_contents)
        for i in tqdm(range(self.multiplier), desc="Batch of fabricated telemetries", position=1):
            for monkey in monkeys:
                monkey.change_fake_data()
            fake_telem_batch = copy.deepcopy(telems)
            SampleMultiplier.fabricate_monkeys_in_telems(fake_telem_batch, monkeys)
            SampleMultiplier.offset_telem_times(iteration=i, telems=fake_telem_batch)
            SampleFileParser.save_teletries_to_files(fake_telem_batch)
            LOGGER.info("")

    @staticmethod
    def fabricate_monkeys_in_telems(telems: List[Dict], monkeys: List[FakeMonkey]):
        for telem in tqdm(telems, desc="Telemetries fabricated", position=2):
            for monkey in monkeys:
                if monkey.on_island:
                    continue
                if (monkey.original_guid in telem['content'] or monkey.original_guid in telem['endpoint']) \
                        and not monkey.on_island:
                    telem['content'] = telem['content'].replace(monkey.original_guid, monkey.fake_guid)
                    telem['endpoint'] = telem['endpoint'].replace(monkey.original_guid, monkey.fake_guid)
                for i in range(len(monkey.original_ips)):
                    telem['content'] = telem['content'].replace(monkey.original_ips[i], monkey.fake_ips[i])

    @staticmethod
    def offset_telem_times(iteration: int, telems: List[Dict]):
        for telem in telems:
            telem['time']['$date'] += iteration * 1000

    def get_monkeys_from_telems(self, telems: List[Dict]):
        island_ips = SampleMultiplier.get_island_ips_from_telems(telems)
        monkeys = []
        for telem in [telem for telem in telems
                      if 'telem_category' in telem and telem['telem_category'] == 'system_info']:
            if 'network_info' not in telem['data']:
                continue
            guid = telem['monkey_guid']
            monkey_present = [monkey for monkey in monkeys if monkey.original_guid == guid]
            if not monkey_present:
                ips = [net_info['addr'] for net_info in telem['data']['network_info']['networks']]
                if set(island_ips).intersection(ips):
                    on_island = True
                else:
                    on_island = False

                monkeys.append(FakeMonkey(ips=ips,
                                          guid=guid,
                                          fake_ip_generator=self.fake_ip_generator,
                                          on_island=on_island))
        return monkeys

    @staticmethod
    def get_island_ips_from_telems(telems: List[Dict]) -> List[str]:
        island_ips = []
        for telem in telems:
            if 'config' in telem:
                island_ips = telem['config']['command_servers']
                for i in range(len(island_ips)):
                    island_ips[i] = island_ips[i].replace(":5000", "")
        return island_ips


if __name__ == "__main__":
    SampleMultiplier(multiplier=int(sys.argv[1])).multiply_telems()
