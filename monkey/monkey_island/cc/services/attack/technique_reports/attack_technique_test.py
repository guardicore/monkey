from unittest import TestCase

from common.utils.attack_utils import ScanStatus

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
                    'value': False  # this field denotes whether technique is enabled or disabled in config
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
            'status': 0,
            'title': 'Unscanned technique'
        },
        set_config(True),  # configuration
        ScanStatus.UNSCANNED.value  # expected status
    ),

    # scanned
    (
        {  # telemetry data
            'info': [],
            'message': 'Scanned',
            'status': 1,
            'title': 'Scanned technique'
        },
        set_config(True),  # configuration
        ScanStatus.SCANNED.value  # expected status
    ),

    # used
    (
        {  # telemetry data
            'info': [],
            'message': 'Used',
            'status': 2,
            'title': 'Used technique'
        },
        set_config(True),  # configuration
        ScanStatus.USED.value  # expected status
    ),

    # disabled
    (
        {  # telemetry data
            'info': [],
            'message': 'Disabled',
            'status': 0,
            'title': 'Disabled technique'
        },
        set_config(False),  # configuration
        ScanStatus.DISABLED.value  # expected status
    )
]


class TestAttackTechnique(TestCase):
    def test__check_status(self):
        for telem_data, config, expected_status in param_list:
            with self.subTest(msg=f"Checking if correct status is returned (status: {telem_data['message']})"):
                self.assertEqual(T9999._check_status(telem_data['status']), expected_status)
