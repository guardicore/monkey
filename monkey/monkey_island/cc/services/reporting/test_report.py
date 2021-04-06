import datetime
from copy import deepcopy

from monkey_island.cc.services.reporting.report import ReportService

NODE_DICT = {
    'id': '602f62118e30cf35830ff8e4',
    'label': 'WinDev2010Eval.mshome.net',
    'group': 'monkey_windows',
    'os': 'windows',
    'dead': True,
    'exploits': [{'result': True,
                  'exploiter': 'DrupalExploiter',
                  'info': {'display_name': 'Drupal Server',
                           'started': datetime.datetime(2021, 2, 19, 9, 0, 14, 950000),
                           'finished': datetime.datetime(2021, 2, 19, 9, 0, 14, 950000),
                           'vulnerable_urls': [],
                           'vulnerable_ports': [],
                           'executed_cmds': []},
                  'attempts': [],
                  'timestamp': datetime.datetime(2021, 2, 19, 9, 0, 14, 984000),
                  'origin': 'MonkeyIsland : 192.168.56.1'},

                 {'result': True,
                  'exploiter': 'ElasticGroovyExploiter',
                  'info': {'display_name': 'Elastic search',
                           'started': datetime.datetime(2021, 2, 19, 9, 0, 15, 16000),
                           'finished': datetime.datetime(2021, 2, 19, 9, 0, 15, 17000),
                           'vulnerable_urls': [], 'vulnerable_ports': [], 'executed_cmds': []},
                  'attempts': [],
                  'timestamp': datetime.datetime(2021, 2, 19, 9, 0, 15, 60000),
                  'origin': 'MonkeyIsland : 192.168.56.1'}]
}

NODE_DICT_DUPLICATE_EXPLOITS = deepcopy(NODE_DICT)
NODE_DICT_DUPLICATE_EXPLOITS['exploits'][1] = NODE_DICT_DUPLICATE_EXPLOITS['exploits'][0]

NODE_DICT_FAILED_EXPLOITS = deepcopy(NODE_DICT)
NODE_DICT_FAILED_EXPLOITS['exploits'][0]['result'] = False
NODE_DICT_FAILED_EXPLOITS['exploits'][1]['result'] = False


def test_get_exploits_used_on_node():
    exploits = ReportService.get_exploits_used_on_node(NODE_DICT)
    assert sorted(exploits) == sorted(['Elastic Groovy Exploiter', 'Drupal Server Exploiter'])

    exploits = ReportService.get_exploits_used_on_node(NODE_DICT_DUPLICATE_EXPLOITS)
    assert exploits == ['Drupal Server Exploiter']

    exploits = ReportService.get_exploits_used_on_node(NODE_DICT_FAILED_EXPLOITS)
    assert exploits == []
