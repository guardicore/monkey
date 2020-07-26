import copy
from unittest import TestCase
from unittest.mock import patch

from common.utils.attack_utils import ScanStatus
from monkey_island.cc.services.attack.attack_config import AttackConfig

from .pba_technique import PostBreachTechnique


class T9999(PostBreachTechnique):
    tech_id = "T9999"
    unscanned_msg = "Unscanned"
    scanned_msg = "Scanned"
    used_msg = "Used"
    pba_names = ["PBA Name"]


config =\
    {
        'category': {
            'link': '',
            'properties': {
                'T9999': {
                    'description': '',
                    'link': '',
                    'necessary': False,
                    'title': '',
                    'type': 'bool',
                    'value': None  # denotes whether technique is enabled/disabled in config (set below in param_list)
                }
            }
        }
    }


def set_config(value: bool):
    config['category']['properties']['T9999']['value'] = value
    return config


param_list = [
    # unscanned
    (
        {  # telemetry data
            'info': [],
            'message': 'Unscanned',
            'status': ScanStatus.UNSCANNED.value,
            'title': 'Unscanned technique'
        },
        copy.deepcopy(set_config(True)),  # configuration
        ScanStatus.UNSCANNED.value  # expected status
    ),

    # scanned
    (
        {  # telemetry data
            'info': [],
            'message': 'Scanned',
            'status': ScanStatus.SCANNED.value,
            'title': 'Scanned technique'
        },
        copy.deepcopy(set_config(True)),  # configuration
        ScanStatus.SCANNED.value  # expected status
    ),

    # used
    (
        {  # telemetry data
            'info': [],
            'message': 'Used',
            'status': ScanStatus.USED.value,
            'title': 'Used technique'
        },
        copy.deepcopy(set_config(True)),  # configuration
        ScanStatus.USED.value  # expected status
    ),

    # disabled
    (
        {  # telemetry data
            'info': [],
            'message': 'Disabled',
            'status': ScanStatus.UNSCANNED.value,
            'title': 'Disabled technique'
        },
        copy.deepcopy(set_config(False)),  # configuration
        ScanStatus.DISABLED.value  # expected status
    )
]


class TestAttackTechnique(TestCase):
    def test__check_status(self):
        for telem_data, config, expected_status in param_list:
            with self.subTest(msg=f"Checking if correct status is returned (status: {telem_data['message']})"):
                with patch.object(AttackConfig, 'get_config', return_value=config):
                    self.assertEqual(T9999._check_status(telem_data['status']), expected_status)
