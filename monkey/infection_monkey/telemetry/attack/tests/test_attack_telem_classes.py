import pytest

from common.utils.attack_utils import ScanStatus, UsageEnum
from infection_monkey.model import VictimHost
from infection_monkey.telemetry.attack.attack_telem import AttackTelem
from infection_monkey.telemetry.attack.usage_telem import UsageTelem
from infection_monkey.telemetry.attack.victim_host_telem import VictimHostTelem

MACHINE = VictimHost('127.0.0.1')
STATUS = ScanStatus.USED
TECHNIQUE = 'T9999'
USAGE = UsageEnum.SMB


@pytest.fixture
def attack_telem_test_instance():
    return AttackTelem(TECHNIQUE, STATUS)


def test_attack_telem_category(attack_telem_test_instance):
    assert attack_telem_test_instance.telem_category == 'attack'


def test_attack_telem_get_data(attack_telem_test_instance):
    actual_data = attack_telem_test_instance.get_data()
    expected_data = {'status': STATUS.value,
                     'technique': TECHNIQUE}
    assert actual_data == expected_data


@pytest.fixture
def usage_telem_test_instance():
    return UsageTelem(TECHNIQUE, STATUS, USAGE)


def test_usage_telem_category(usage_telem_test_instance):
    assert usage_telem_test_instance.telem_category == 'attack'


def test_usage_telem_get_data(usage_telem_test_instance):
    actual_data = usage_telem_test_instance.get_data()
    expected_data = {'status': STATUS.value,
                     'technique': TECHNIQUE,
                     'usage': USAGE.name}
    assert actual_data == expected_data


@pytest.fixture
def victim_host_telem_test_instance():
    return VictimHostTelem(TECHNIQUE, STATUS, MACHINE)


def test_victim_host_telem_category(victim_host_telem_test_instance):
    assert victim_host_telem_test_instance.telem_category == 'attack'


def test_victim_host_telem_get_data(victim_host_telem_test_instance):
    actual_data = victim_host_telem_test_instance.get_data()
    expected_data = {'machine': {'domain_name': MACHINE.domain_name,
                                 'ip_addr': MACHINE.ip_addr},
                     'status': STATUS.value,
                     'technique': TECHNIQUE}
    assert actual_data == expected_data
