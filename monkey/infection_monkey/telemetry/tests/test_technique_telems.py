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


COMMAND = 'echo hi'
DST_IP = '0.0.0.1'
FILENAME = 'virus.exe'
GATHERED_DATA_TYPE = '[Type of data collected]'
INFO = '[Additional info]'
MACHINE = VictimHost('127.0.0.1')
PATH = 'path/to/file.txt'
SRC_IP = '0.0.0.0'
STATUS = ScanStatus.USED
USAGE = UsageEnum.SMB
USAGE_STR = '[Usage info]'


@pytest.fixture
def T1005_telem_test_instance():
    return T1005Telem(STATUS, GATHERED_DATA_TYPE, INFO)


def test_T1005_send(T1005_telem_test_instance, spy_send_telemetry):
    T1005_telem_test_instance.send()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1005',
                     'gathered_data_type': GATHERED_DATA_TYPE,
                     'info': INFO}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'


@pytest.fixture
def T1035_telem_test_instance():
    return T1035Telem(STATUS, USAGE)


def test_T1035_send(T1035_telem_test_instance, spy_send_telemetry):
    T1035_telem_test_instance.send()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1035',
                     'usage': USAGE.name}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'


@pytest.fixture
def T1064_telem_test_instance():
    return T1064Telem(STATUS, USAGE_STR)


def test_T1064_send(T1064_telem_test_instance, spy_send_telemetry):
    T1064_telem_test_instance.send()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1064',
                     'usage': USAGE_STR}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'


@pytest.fixture
def T1105_telem_test_instance():
    return T1105Telem(STATUS, SRC_IP, DST_IP, FILENAME)


def test_T1105_send(T1105_telem_test_instance, spy_send_telemetry):
    T1105_telem_test_instance.send()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1105',
                     'filename': FILENAME,
                     'src': SRC_IP,
                     'dst': DST_IP}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'


@pytest.fixture
def T1106_telem_test_instance():
    return T1106Telem(STATUS, USAGE)


def test_T1106_send(T1106_telem_test_instance, spy_send_telemetry):
    T1106_telem_test_instance.send()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1106',
                     'usage': USAGE.name}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'


@pytest.fixture
def T1107_telem_test_instance():
    return T1107Telem(STATUS, PATH)


def test_T1107_send(T1107_telem_test_instance, spy_send_telemetry):
    T1107_telem_test_instance.send()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1107',
                     'path': PATH}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'


@pytest.fixture
def T1129_telem_test_instance():
    return T1129Telem(STATUS, USAGE)


def test_T1129_send(T1129_telem_test_instance, spy_send_telemetry):
    T1129_telem_test_instance.send()
    expected_data = {'status': STATUS.value,
                     'technique': 'T1129',
                     'usage': USAGE.name}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'


@pytest.fixture
def T1197_telem_test_instance():
    return T1197Telem(STATUS, MACHINE, USAGE_STR)


def test_T1197_send(T1197_telem_test_instance, spy_send_telemetry):
    T1197_telem_test_instance.send()
    expected_data = {'machine': {'domain_name': MACHINE.domain_name,
                                 'ip_addr': MACHINE.ip_addr},
                     'status': STATUS.value,
                     'technique': 'T1197',
                     'usage': USAGE_STR}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'


@pytest.fixture
def T1222_telem_test_instance():
    return T1222Telem(STATUS, COMMAND, MACHINE)


def test_T1222_send(T1222_telem_test_instance, spy_send_telemetry):
    T1222_telem_test_instance.send()
    expected_data = {'machine': {'domain_name': MACHINE.domain_name,
                                 'ip_addr': MACHINE.ip_addr},
                     'status': STATUS.value,
                     'technique': 'T1222',
                     'command': COMMAND}
    assert spy_send_telemetry.data == expected_data
    assert spy_send_telemetry.telem_category == 'attack'
