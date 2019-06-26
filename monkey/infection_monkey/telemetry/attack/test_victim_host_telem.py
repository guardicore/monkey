from unittest import TestCase

from common.utils.attack_utils import ScanStatus
from infection_monkey.model import VictimHost
from infection_monkey.telemetry.attack.victim_host_telem import VictimHostTelem


class TestVictimHostTelem(TestCase):
    def test_get_data(self):
        machine = VictimHost('127.0.0.1')
        status = ScanStatus.USED
        technique = 'T1210'

        telem = VictimHostTelem(technique, status, machine)

        self.assertEqual(telem.telem_category, 'attack')

        expected_data = {
            'machine': {
                'domain_name': machine.domain_name,
                'ip_addr': machine.ip_addr
            },
            'status': status.value,
            'technique': technique
        }

        actual_data = telem.get_data()

        self.assertEqual(actual_data, expected_data)
