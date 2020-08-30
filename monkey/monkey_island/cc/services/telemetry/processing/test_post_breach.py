from unittest.mock import Mock

import monkey_island.cc.services.telemetry.processing.post_breach as post_breach

from .post_breach import EXECUTION_WITHOUT_OUTPUT

original_telem_multiple_results =\
    {
        'data': {
            'command': 'COMMAND',
            'hostname': 'HOST',
            'ip': '127.0.1.1',
            'name': 'PBA NAME',
            'result': [
                ['SUCCESSFUL', True],
                ['UNSUCCESFUL', False],
                ['', True]
            ]
        },
        'telem_category': 'post_breach'
    }

expected_telem_multiple_results =\
    {
        'data': [
            {
                'command': 'COMMAND',
                'hostname': 'HOST',
                'ip': '127.0.1.1',
                'name': 'PBA NAME',
                'result': ['SUCCESSFUL', True]
            },
            {
                'command': 'COMMAND',
                'hostname': 'HOST',
                'ip': '127.0.1.1',
                'name': 'PBA NAME',
                'result': ['UNSUCCESFUL', False]
            },
            {
                'command': 'COMMAND',
                'hostname': 'HOST',
                'ip': '127.0.1.1',
                'name': 'PBA NAME',
                'result': [EXECUTION_WITHOUT_OUTPUT, True]
            }
        ],
        'telem_category': 'post_breach'
    }

original_telem_single_result =\
    {
        'data': {
            'command': 'COMMAND',
            'hostname': 'HOST',
            'ip': '127.0.1.1',
            'name': 'PBA NAME',
            'result': ['', True]
        },
        'telem_category': 'post_breach'
    }

expected_telem_single_result =\
    {
        'data': [
            {
                'command': 'COMMAND',
                'hostname': 'HOST',
                'ip': '127.0.1.1',
                'name': 'PBA NAME',
                'result': [EXECUTION_WITHOUT_OUTPUT, True]
            },
        ],
        'telem_category': 'post_breach'
    }


def test_process_post_breach_telemetry():
    post_breach.update_data = Mock()  # actual behavior of update_data() is to access mongodb
    # multiple results in PBA
    post_breach.process_post_breach_telemetry(original_telem_multiple_results)
    assert original_telem_multiple_results == expected_telem_multiple_results
    # single result in PBA
    post_breach.process_post_breach_telemetry(original_telem_single_result)
    assert original_telem_single_result == expected_telem_single_result
