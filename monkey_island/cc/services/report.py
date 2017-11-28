import ipaddress

from cc.database import mongo
from cc.services.edge import EdgeService
from cc.services.node import NodeService
from cc.utils import local_ip_addresses, get_subnets

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
            st += "%d days, " % delta.days
        total = delta.seconds
        seconds = total % 60
        total = (total - seconds) / 60
        minutes = total % 60
        total = (total - minutes) / 60
        hours = total
        if hours > 0:
            st += "%d hours, " % hours

        st += "%d minutes and %d seconds" % (minutes, seconds)
        return st

    @staticmethod
    def get_tunnels():
        return [
            {
                'type': 'tunnel',
                'origin': NodeService.get_node_hostname(NodeService.get_node_or_monkey_by_id(tunnel['_id'])),
                'dest': NodeService.get_node_hostname(NodeService.get_node_or_monkey_by_id(tunnel['tunnel']))
            }
            for tunnel in mongo.db.monkey.find({'tunnel': {'$exists': True}}, {'tunnel': 1})]

    @staticmethod
    def get_scanned():
        nodes = \
            [NodeService.get_displayed_node_by_id(node['_id']) for node in mongo.db.node.find({}, {'_id': 1})] \
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
    def get_exploited():
        exploited = \
            [NodeService.get_displayed_node_by_id(monkey['_id']) for monkey in mongo.db.monkey.find({}, {'_id': 1})
             if not NodeService.get_monkey_manual_run(NodeService.get_monkey_by_id(monkey['_id']))] \
            + [NodeService.get_displayed_node_by_id(node['_id'])
               for node in mongo.db.node.find({'exploited': True}, {'_id': 1})]

        exploited = [
            {
                'label': NodeService.get_node_hostname(NodeService.get_node_or_monkey_by_id(monkey['id'])),
                'ip_addresses': monkey['ip_addresses'],
                'exploits': [exploit['exploiter'] for exploit in monkey['exploits'] if exploit['result']]
            }
            for monkey in exploited]

        return exploited

    @staticmethod
    def get_stolen_creds():
        PASS_TYPE_DICT = {'password': 'Clear Password', 'lm_hash': 'LM', 'ntlm_hash': 'NTLM'}
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
                            'type': PASS_TYPE_DICT[pass_type],
                            'origin': origin
                        }
                    )
        return creds

    @staticmethod
    def process_general_exploit(exploit):
        ip_addr = exploit['data']['machine']['ip_addr']
        return {'machine': NodeService.get_node_hostname(NodeService.get_node_or_monkey_by_ip(ip_addr)),
                'ip_address': ip_addr}

    @staticmethod
    def process_general_creds_exploit(exploit):
        processed_exploit = ReportService.process_general_exploit(exploit)

        for attempt in exploit['data']['attempts']:
            if attempt['result']:
                processed_exploit['username'] = attempt['user']
                if len(attempt['password']) > 0:
                    processed_exploit['type'] = 'password'
                else:
                    processed_exploit['type'] = 'hash'
                return processed_exploit

    @staticmethod
    def process_smb_exploit(exploit):
        processed_exploit = ReportService.process_general_creds_exploit(exploit)
        if processed_exploit['type'] == 'password':
            processed_exploit['type'] = 'smb_password'
        else:
            processed_exploit['type'] = 'smb_pth'
        return processed_exploit

    @staticmethod
    def process_wmi_exploit(exploit):
        processed_exploit = ReportService.process_general_creds_exploit(exploit)
        if processed_exploit['type'] == 'password':
            processed_exploit['type'] = 'wmi_password'
        else:
            processed_exploit['type'] = 'wmi_pth'
        return processed_exploit

    @staticmethod
    def process_ssh_exploit(exploit):
        processed_exploit = ReportService.process_general_creds_exploit(exploit)
        processed_exploit['type'] = 'ssh'
        return processed_exploit

    @staticmethod
    def process_rdp_exploit(exploit):
        processed_exploit = ReportService.process_general_creds_exploit(exploit)
        processed_exploit['type'] = 'rdp'
        return processed_exploit

    @staticmethod
    def process_sambacry_exploit(exploit):
        processed_exploit = ReportService.process_general_creds_exploit(exploit)
        processed_exploit['type'] = 'sambacry'
        return processed_exploit

    @staticmethod
    def process_elastic_exploit(exploit):
        processed_exploit = ReportService.process_general_exploit(exploit)
        processed_exploit['type'] = 'elastic'
        return processed_exploit

    @staticmethod
    def process_conficker_exploit(exploit):
        processed_exploit = ReportService.process_general_exploit(exploit)
        processed_exploit['type'] = 'conficker'
        return processed_exploit

    @staticmethod
    def process_shellshock_exploit(exploit):
        processed_exploit = ReportService.process_general_exploit(exploit)
        processed_exploit['type'] = 'shellshock'
        urls = exploit['data']['info']['vulnerable_urls']
        processed_exploit['port'] = urls[0].split(':')[2].split('/')[0]
        processed_exploit['paths'] = ['/' + url.split(':')[2].split('/')[1] for url in urls]
        return processed_exploit

    @staticmethod
    def process_exploit(exploit):
        exploiter_type = exploit['data']['exploiter']
        if exploiter_type == 'SmbExploiter':
            return ReportService.process_smb_exploit(exploit)
        if exploiter_type == 'WmiExploiter':
            return ReportService.process_wmi_exploit(exploit)
        if exploiter_type == 'SSHExploiter':
            return ReportService.process_ssh_exploit(exploit)
        if exploiter_type == 'RdpExploiter':
            return ReportService.process_rdp_exploit(exploit)
        if exploiter_type == 'SambaCryExploiter':
            return ReportService.process_sambacry_exploit(exploit)
        if exploiter_type == 'ElasticGroovyExploiter':
            return ReportService.process_elastic_exploit(exploit)
        if exploiter_type == 'Ms08_067_Exploiter':
            return ReportService.process_conficker_exploit(exploit)
        if exploiter_type == 'ShellShockExploiter':
            return ReportService.process_shellshock_exploit(exploit)

    @staticmethod
    def get_exploits():
        exploits = []
        for exploit in mongo.db.telemetry.find({'telem_type': 'exploit', 'data.result': True}):
            new_exploit = ReportService.process_exploit(exploit)
            if new_exploit not in exploits:
                exploits.append(new_exploit)
        return exploits

    @staticmethod
    def get_monkey_subnets(monkey_guid):
        return \
            [
                ipaddress.ip_interface(unicode(network['addr'] + '/' + network['netmask'])).network
                for network in
                mongo.db.telemetry.find_one(
                    {'telem_type': 'system_info_collection', 'monkey_guid': monkey_guid},
                    {'data.network_info.networks': 1}
                )['data']['network_info']['networks']
            ]

    @staticmethod
    def get_cross_segment_issues():
        issues = []
        island_ips = local_ip_addresses()
        for monkey in mongo.db.monkey.find({'tunnel': {'$exists': False}}, {'tunnel': 1, 'guid': 1, 'hostname': 1}):
            found_good_ip = False
            monkey_subnets = ReportService.get_monkey_subnets(monkey['guid'])
            for subnet in monkey_subnets:
                for ip in island_ips:
                    if ipaddress.ip_address(unicode(ip)) in subnet:
                        found_good_ip = True
                        break
                if found_good_ip:
                    break
            if not found_good_ip:
                issues.append(
                    {'type': 'cross_segment', 'machine': monkey['hostname'],
                     'networks': [str(subnet) for subnet in monkey_subnets],
                     'server_networks': [str(subnet) for subnet in get_subnets()]}
                )

        return issues

    @staticmethod
    def get_issues():
        return ReportService.get_exploits() + ReportService.get_tunnels() + ReportService.get_cross_segment_issues()

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
                        'issues': ReportService.get_issues()
                    }
            }

    @staticmethod
    def did_exploit_type_succeed(exploit_type):
        return mongo.db.edge.count(
            {'exploits': {'$elemMatch': {'exploiter': exploit_type, 'result': True}}},
            limit=1) > 0
