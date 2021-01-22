import pytest

from common.utils.attack_utils import ScanStatus, UsageEnum
from infection_monkey.model import VictimHost
from infection_monkey.telemetry.attack.t1005_telem import T1005Telem
from infection_monkey.telemetry.attack.t1035_telem import T1035Telem
from infection_monkey.telemetry.attack.t1064_telem import T1064Telem
from infection_monkey.telemetry.attack.t1105_telem import T1105Telem
from infection_monkey.telemetry.attack.t1106_telem import T1106Telem
from infection_monkey.telemetry.attack.t1107_telem import T1107Telem
from infection_monkey.telemetry.attack.t1129_telem import T1129Telem
from infection_monkey.telemetry.attack.t1197_telem import T1197Telem
from infection_monkey.telemetry.attack.t1222_telem import T1222Telem

GATHERED_DATA_TYPE = '[Type of data collected]'
INFO = '[Additional info]'
MACHINE = VictimHost('127.0.0.1')
STATUS = ScanStatus.USED
USAGE = UsageEnum.SMB
SRC_IP = '0.0.0.0'
DST_IP = '0.0.0.1'
FILENAME = 'virus.exe'
PATH = 'path/to/file.txt'
COMMAND = 'echo hi'


@pytest.fixture
def T1005_telem_test_instance():
    return T1005Telem(STATUS, GATHERED_DATA_TYPE, INFO)


def test_T1005_telem_category(T1005_telem_test_instance):
    assert T1005_telem_test_instance.telem_category == 'attack'


def test_T1005_get_data(T1005_telem_test_instance):
    actual_data = T1005_telem_test_instance.get_data()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1005',
                     'gathered_data_type': GATHERED_DATA_TYPE,
                     'info': INFO}
    assert actual_data == expected_data


@pytest.fixture
def T1035_telem_test_instance():
    return T1035Telem(STATUS, USAGE)


def test_T1035_telem_category(T1035_telem_test_instance):
    assert T1035_telem_test_instance.telem_category == 'attack'


def test_T1035_get_data(T1035_telem_test_instance):
    actual_data = T1035_telem_test_instance.get_data()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1035',
                     'usage': USAGE.name}
    assert actual_data == expected_data


@pytest.fixture
def T1064_telem_test_instance():
    return T1064Telem(STATUS, USAGE)


def test_T1064_telem_category(T1064_telem_test_instance):
    assert T1064_telem_test_instance.telem_category == 'attack'


def test_T1064_get_data(T1064_telem_test_instance):
    actual_data = T1064_telem_test_instance.get_data()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1064',
                     'usage': USAGE}
    assert actual_data == expected_data


@pytest.fixture
def T1105_telem_test_instance():
    return T1105Telem(STATUS, SRC_IP, DST_IP, FILENAME)


def test_T1105_telem_category(T1105_telem_test_instance):
    assert T1105_telem_test_instance.telem_category == 'attack'


def test_T1105_get_data(T1105_telem_test_instance):
    actual_data = T1105_telem_test_instance.get_data()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1105',
                     'filename': FILENAME,
                     'src': SRC_IP,
                     'dst': DST_IP}
    assert actual_data == expected_data


@pytest.fixture
def T1106_telem_test_instance():
    return T1106Telem(STATUS, USAGE)


def test_T1106_telem_category(T1106_telem_test_instance):
    assert T1106_telem_test_instance.telem_category == 'attack'


def test_T1106_get_data(T1106_telem_test_instance):
    actual_data = T1106_telem_test_instance.get_data()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1106',
                     'usage': USAGE.name}
    assert actual_data == expected_data


@pytest.fixture
def T1107_telem_test_instance():
    return T1107Telem(STATUS, PATH)


def test_T1107_telem_category(T1107_telem_test_instance):
    assert T1107_telem_test_instance.telem_category == 'attack'


def test_T1107_get_data(T1107_telem_test_instance):
    actual_data = T1107_telem_test_instance.get_data()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1107',
                     'path': PATH}
    assert actual_data == expected_data


@pytest.fixture
def T1129_telem_test_instance():
    return T1129Telem(STATUS, USAGE)


def test_T1129_telem_category(T1129_telem_test_instance):
    assert T1129_telem_test_instance.telem_category == 'attack'


def test_T1129_get_data(T1129_telem_test_instance):
    actual_data = T1129_telem_test_instance.get_data()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1129',
                     'usage': USAGE.name}
    assert actual_data == expected_data


@pytest.fixture
def T1197_telem_test_instance():
    return T1197Telem(STATUS, MACHINE, USAGE)


def test_T1197_telem_category(T1197_telem_test_instance):
    assert T1197_telem_test_instance.telem_category == 'attack'


def test_T1197_get_data(T1197_telem_test_instance):
    actual_data = T1197_telem_test_instance.get_data()
    expected_data = {'machine': {'domain_name': MACHINE.domain_name,
                                 'ip_addr': MACHINE.ip_addr},
                     'status': STATUS.value,
                     'technique': 'T1197',
                     'usage': USAGE}
    assert actual_data == expected_data


@pytest.fixture
def T1222_telem_test_instance():
    return T1222Telem(STATUS, COMMAND, MACHINE)


def test_T1222_telem_category(T1222_telem_test_instance):
    assert T1222_telem_test_instance.telem_category == 'attack'


def test_T1222_get_data(T1222_telem_test_instance):
    actual_data = T1222_telem_test_instance.get_data()
    expected_data = {'machine': {'domain_name': MACHINE.domain_name,
                                 'ip_addr': MACHINE.ip_addr},
                     'status': STATUS.value,
                     'technique': 'T1222',
                     'command': COMMAND}
    assert actual_data == expected_data
