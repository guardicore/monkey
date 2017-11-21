import datetime

from cc.database import mongo
from cc.services.config import ConfigService
from cc.services.edge import EdgeService
from cc.services.node import NodeService

__author__ = "itay.mizeretz"


class ReportService:
    def __init__(self):
        pass

    @staticmethod
    def get_first_monkey_time():
        return mongo.db.telemetry.find({}, {'timestamp': 1}).sort([('$natural', 1)]).limit(1)[0]['timestamp']

    @staticmethod
    def get_last_monkey_dead_time():
        return mongo.db.telemetry.find({}, {'timestamp': 1}).sort([('$natural', -1)]).limit(1)[0]['timestamp']

    @staticmethod
    def get_monkey_duration():
        delta = ReportService.get_last_monkey_dead_time() - ReportService.get_first_monkey_time()
        st = ""
        if delta.days > 0:
            st += "%d days," % delta.days
        total = delta.seconds
        seconds = total % 60
        total = (total - seconds) / 60
        minutes = total % 60
        total = (total - minutes) / 60
        hours = total
        if hours > 0:
            st += "%d hours," % hours

        st += "%d minutes and %d seconds" % (minutes, seconds)
        return st

    @staticmethod
    def get_breach_count():
        return mongo.db.edge.count({'exploits.result': True})

    @staticmethod
    def get_successful_exploit_types():
        exploit_types = mongo.db.command({'distinct': 'edge', 'key': 'exploits.exploiter'})['values']
        return [exploit for exploit in exploit_types if ReportService.did_exploit_type_succeed(exploit)]

    @staticmethod
    def get_tunnels():
        return [
            (NodeService.get_monkey_label_by_id(tunnel['_id']), NodeService.get_monkey_label_by_id(tunnel['tunnel']))
            for tunnel in mongo.db.monkey.find({'tunnel': {'$exists': True}}, {'tunnel': 1})]

    @staticmethod
    def get_scanned():
        nodes =\
            [NodeService.get_displayed_node_by_id(node['_id']) for node in mongo.db.node.find({}, {'_id': 1})]\
            + [NodeService.get_displayed_node_by_id(monkey['_id']) for monkey in mongo.db.monkey.find({}, {'_id': 1})]
        nodes = [
            {
                'label':
                    node['hostname'] if 'hostname' in node else NodeService.get_node_by_id(node['id'])['os']['version'],
                'ip_addresses': node['ip_addresses'],
                'accessible_from_nodes':
                    (x['hostname'] for x in
                     (NodeService.get_displayed_node_by_id(edge['from'])
                      for edge in EdgeService.get_displayed_edges_by_to(node['id']))),
                'services': node['services']
            }
            for node in nodes]

        return nodes

    @staticmethod
    def get_reused_passwords():
        password_dict = {}
        password_list = ConfigService.get_config_value(['basic', 'credentials', 'exploit_password_list'])
        for password in password_list:
            machines_with_password =\
                [
                    NodeService.get_monkey_label_by_id(node['_id'])
                    for node in mongo.db.monkey.find({'creds.password': password}, {'_id': 1})
                ]
            if len(machines_with_password) >= 2:
                password_dict[password] = machines_with_password

        return password_dict

    @staticmethod
    def get_exploited():
        exploited =\
            [NodeService.get_displayed_node_by_id(monkey['_id']) for monkey in mongo.db.monkey.find({}, {'_id': 1})
             if not NodeService.get_monkey_manual_run(NodeService.get_monkey_by_id(monkey['_id']))]\
            + [NodeService.get_displayed_node_by_id(node['_id'])
               for node in mongo.db.node.find({'exploited': True}, {'_id': 1})]

        exploited = [
            {
                'label': monkey['hostname'] if 'hostname' in monkey else monkey['os']['version'],
                'ip_addresses': monkey['ip_addresses'],
                'exploits': [exploit['exploiter'] for exploit in monkey['exploits'] if exploit['result']]
            }
            for monkey in exploited]

        return exploited

    @staticmethod
    def get_stolen_creds():
        PASS_TYPE_DICT = {'password': 'Password', 'lm_hash': 'LM', 'ntlm_hash': 'NTLM'}
        creds = []
        for telem in mongo.db.telemetry.find(
            {'telem_type': 'system_info_collection', 'data.credentials': {'$exists': True}},
            {'data.credentials': 1, 'monkey_guid': 1}
        ):
            monkey_creds = telem['data']['credentials']
            if len(monkey_creds) == 0:
                continue
            origin = NodeService.get_monkey_by_guid(telem['monkey_guid'])['hostname']
            for user in monkey_creds:
                for pass_type in monkey_creds[user]:
                    creds.append(
                        {
                            'username': user,
                            'password': monkey_creds[user][pass_type],
                            'type': PASS_TYPE_DICT[pass_type],
                            'origin': origin
                        }
                    )
        return creds

    @staticmethod
    def get_report():
        return \
            {
                'overview':
                    {
                        'monkey_start_time': ReportService.get_first_monkey_time().strftime("%d/%m/%Y %H:%M:%S"),
                        'monkey_duration': ReportService.get_monkey_duration(),
                        'issues': [False, True, True, True, False, True],
                        'warnings': [True, True]
                    },
                'glance':
                    {
                        'scanned': ReportService.get_scanned(),
                        'exploited': ReportService.get_exploited(),
                        'stolen_creds': ReportService.get_stolen_creds()
                    },
                'recommendations':
                    {
                        'issues':
                            [
                                {'type': 'smb_password', 'machine': 'Monkey-SMB',
                                 'ip_addresses': ['192.168.0.1', '10.0.0.18'], 'username': 'Administrator'},
                                {'type': 'smb_pth', 'machine': 'Monkey-SMB2', 'ip_addresses': ['192.168.0.1', '10.0.0.18'],
                                 'username': 'Administrator'},
                                {'type': 'wmi_password', 'machine': 'Monkey-WMI',
                                 'ip_addresses': ['192.168.0.1', '10.0.0.18'], 'username': 'Administrator'},
                                {'type': 'wmi_pth', 'machine': 'Monkey-WMI2', 'ip_addresses': ['192.168.0.1', '10.0.0.18'],
                                 'username': 'Administrator'},
                                {'type': 'ssh', 'machine': 'Monkey-SMB', 'ip_addresses': ['192.168.0.1', '10.0.0.18'],
                                 'username': 'Administrator'},
                                {'type': 'rdp', 'machine': 'Monkey-SMB', 'ip_addresses': ['192.168.0.1', '10.0.0.18'],
                                 'username': 'Administrator'},
                                {'type': 'sambacry', 'machine': 'Monkey-SMB', 'ip_addresses': ['192.168.0.1', '10.0.0.18'],
                                 'username': 'Administrator'},
                                {'type': 'elastic', 'machine': 'Monkey-SMB', 'ip_addresses': ['192.168.0.1', '10.0.0.18']},
                                {'type': 'shellshock', 'machine': 'Monkey-SMB', 'ip_addresses': ['192.168.0.1', '10.0.0.18'],
                                 'port': 8080, 'paths': ['/cgi/backserver.cgi', '/cgi/login.cgi']},
                                {'type': 'conficker', 'machine': 'Monkey-SMB', 'ip_addresses': ['192.168.0.1', '10.0.0.18']},
                                {'type': 'cross_segment', 'machine': 'Monkey-SMB', 'network': '192.168.0.0/24',
                                 'server_network': '172.168.0.0/24'},
                                {'type': 'tunnel', 'origin': 'Monkey-SSH', 'dest': 'Monkey-SambaCry'}
                            ]
                    }
            }
        # TODO: put implementation in template
        """
        return \
            {
                'breach_count': ReportService.get_breach_count(),
                'successful_exploit_types': ReportService.get_successful_exploit_types(),
                'tunnels': ReportService.get_tunnels(),
                'reused_passwords': ReportService.get_reused_passwords()
            }
        """

    @staticmethod
    def did_exploit_type_succeed(exploit_type):
        return mongo.db.edge.count(
            {'exploits': {'$elemMatch': {'exploiter': exploit_type, 'result': True}}},
            limit=1) > 0
