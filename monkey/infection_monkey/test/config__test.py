# -*- coding: UTF-8 -*-
# NOTE: Launch all tests with `nosetests` command from infection_monkey dir.

import json
import unittest

from mock import Mock, patch

import infection_monkey.control as control

from infection_monkey.config import GUID


class ReportConfigErrorTestCase(unittest.TestCase):
    """
    When unknown config variable received form the island server, skip it and report config
    error back to the server.
    """

    config_response = Mock(json=Mock(return_value={'config': {'blah': 'blah'}}))

    def teardown(self):
        patch.stopall()

    def test_config(self):
        patch('control.requests.patch', Mock()).start()
        patch('control.WormConfiguration', Mock(current_server='127.0.0.1:123')).start()

        # GIVEN the server with uknown config variable
        patch('control.requests.get', Mock(return_value=self.config_response)).start()

        # WHEN monkey tries to load config from server
        control.ControlClient.load_control_config()

        # THEN she reports config error back to the server
        control.requests.patch.assert_called_once_with(
                "https://127.0.0.1:123/api/monkey/%s" % GUID,
                data=json.dumps({'config_error': True}),
                headers={'content-type': 'application/json'},
                verify=False,
                proxies=control.ControlClient.proxies)


if __name__ == '__main__':
    unittest.main()
