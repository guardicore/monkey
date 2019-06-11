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

        self.assertEqual(telem.technique, technique)
        self.assertEqual(telem.status, status)
        self.assertEqual(telem.telem_type, 'attack')
        self.assertEqual(telem.machine['domain_name'], machine.domain_name)
        self.assertEqual(telem.machine['ip_addr'], machine.ip_addr)
