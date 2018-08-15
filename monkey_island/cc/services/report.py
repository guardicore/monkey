import ipaddress
import logging
from enum import Enum

from six import text_type

from cc.database import mongo
from cc.services.config import ConfigService
from cc.services.edge import EdgeService
from cc.services.node import NodeService
from cc.utils import local_ip_addresses, get_subnets

__author__ = "itay.mizeretz"


logger = logging.getLogger(__name__)


class ReportService:
    def __init__(self):
        pass

    EXPLOIT_DISPLAY_DICT = \
        {
            'SmbExploiter': 'SMB Exploiter',
            'WmiExploiter': 'WMI Exploiter',
            'SSHExploiter': 'SSH Exploiter',
            'RdpExploiter': 'RDP Exploiter',
            'SambaCryExploiter': 'SambaCry Exploiter',
            'ElasticGroovyExploiter': 'Elastic Groovy Exploiter',
            'Ms08_067_Exploiter': 'Conficker Exploiter',
            'ShellShockExploiter': 'ShellShock Exploiter',
            'Struts2Exploiter': 'Struts2 Exploiter',
            'WebLogicExploiter': 'Oracle WebLogic Exploiter',
            'HadoopExploiter': 'Hadoop/Yarn Exploiter'
        }

    class ISSUES_DICT(Enum):
        WEAK_PASSWORD = 0
        STOLEN_CREDS = 1
        ELASTIC = 2
        SAMBACRY = 3
        SHELLSHOCK = 4
        CONFICKER = 5
        AZURE = 6
        STOLEN_SSH_KEYS = 7
        STRUTS2 = 8
        WEBLOGIC = 9,
        HADOOP = 10

    class WARNINGS_DICT(Enum):
        CROSS_SEGMENT = 0
        TUNNEL = 1

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
        hours, rem = divmod(delta.seconds, 60 * 60)
        minutes, seconds = divmod(rem, 60)

        if delta.days > 0:
            st += "%d days, " % delta.days
        if hours > 0:
            st += "%d hours, " % hours
        st += "%d minutes and %d seconds" % (minutes, seconds)

        return st

    @staticmethod
    def get_tunnels():
        return [
            {
                'type': 'tunnel',
                'machine': NodeService.get_node_hostname(NodeService.get_node_or_monkey_by_id(tunnel['_id'])),
                'dest': NodeService.get_node_hostname(NodeService.get_node_or_monkey_by_id(tunnel['tunnel']))
            }
            for tunnel in mongo.db.monkey.find({'tunnel': {'$exists': True}}, {'tunnel': 1})]

    @staticmethod
    def get_azure_issues():
        creds = ReportService.get_azure_creds()
        machines = set([instance['origin'] for instance in creds])

        logger.info('Azure issues generated for reporting')

        return [
            {
                'type': 'azure_password',
                'machine': machine,
                'users': set([instance['username'] for instance in creds if instance['origin'] == machine])
            }
            for machine in machines]

    @staticmethod
    def get_scanned():
        nodes = \
            [NodeService.get_displayed_node_by_id(node['_id'], True) for node in mongo.db.node.find({}, {'_id': 1})] \
            + [NodeService.get_displayed_node_by_id(monkey['_id'], True) for monkey in
               mongo.db.monkey.find({}, {'_id': 1})]
        nodes = [
            {
                'label': node['label'],
                'ip_addresses': node['ip_addresses'],
                'accessible_from_nodes':
                    (x['hostname'] for x in
                     (NodeService.get_displayed_node_by_id(edge['from'], True)
                      for edge in EdgeService.get_displayed_edges_by_to(node['id'], True))),
                'services': node['services']
            }
            for node in nodes]

        logger.info('Scanned nodes generated for reporting')

        return nodes

    @staticmethod
    def get_exploited():
        exploited = \
            [NodeService.get_displayed_node_by_id(monkey['_id'], True) for monkey in
             mongo.db.monkey.find({}, {'_id': 1})
             if not NodeService.get_monkey_manual_run(NodeService.get_monkey_by_id(monkey['_id']))] \
            + [NodeService.get_displayed_node_by_id(node['_id'], True)
               for node in mongo.db.node.find({'exploited': True}, {'_id': 1})]

        exploited = [
            {
                'label': monkey['label'],
                'ip_addresses': monkey['ip_addresses'],
                'exploits': list(set(
                    [ReportService.EXPLOIT_DISPLAY_DICT[exploit['exploiter']] for exploit in monkey['exploits'] if
                     exploit['result']]))
            }
            for monkey in exploited]

        logger.info('Exploited nodes generated for reporting')

        return exploited

    @staticmethod
    def get_stolen_creds():
        PASS_TYPE_DICT = {'password': 'Clear Password', 'lm_hash': 'LM hash', 'ntlm_hash': 'NTLM hash'}
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
                            'username': user.replace(',', '.'),
                            'type': PASS_TYPE_DICT[pass_type],
                            'origin': origin
                        }
                    )
        logger.info('Stolen creds generated for reporting')
        return creds

    @staticmethod
    def get_ssh_keys():
        """
        Return private ssh keys found as credentials
        :return: List of credentials
        """
        creds = []
        for telem in mongo.db.telemetry.find(
                {'telem_type': 'system_info_collection', 'data.ssh_info': {'$exists': True}},
                {'data.ssh_info': 1, 'monkey_guid': 1}
        ):
            origin = NodeService.get_monkey_by_guid(telem['monkey_guid'])['hostname']
            if telem['data']['ssh_info']:
                # Pick out all ssh keys not yet included in creds
                ssh_keys = [{'username': key_pair['name'], 'type': 'Clear SSH private key',
                             'origin': origin} for key_pair in telem['data']['ssh_info']
                            if key_pair['private_key'] and {'username': key_pair['name'], 'type': 'Clear SSH private key',
                            'origin': origin} not in creds]
                creds.extend(ssh_keys)
        return creds

    @staticmethod
    def get_azure_creds():
        """
        Recover all credentials marked as being from an Azure machine
        :return: List of credentials.
        """
        creds = []
        for telem in mongo.db.telemetry.find(
                {'telem_type': 'system_info_collection', 'data.Azure': {'$exists': True}},
                {'data.Azure': 1, 'monkey_guid': 1}
        ):
            azure_users = telem['data']['Azure']['usernames']
            if len(azure_users) == 0:
                continue
            origin = NodeService.get_monkey_by_guid(telem['monkey_guid'])['hostname']
            azure_leaked_users = [{'username': user.replace(',', '.'), 'type': 'Clear Password',
                                   'origin': origin} for user in azure_users]
            creds.extend(azure_leaked_users)

        logger.info('Azure machines creds generated for reporting')
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
                if attempt['password']:
                    processed_exploit['type'] = 'password'
                    processed_exploit['password'] = attempt['password']
                elif attempt['ssh_key']:
                    processed_exploit['type'] = 'ssh_key'
                    processed_exploit['ssh_key'] = attempt['ssh_key']
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
        # Check if it's ssh key or ssh login credentials exploit
        if processed_exploit['type'] == 'ssh_key':
            return processed_exploit
        else:
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
    def process_struts2_exploit(exploit):
        processed_exploit = ReportService.process_general_exploit(exploit)
        processed_exploit['type'] = 'struts2'
        return processed_exploit

    @staticmethod
    def process_weblogic_exploit(exploit):
        processed_exploit = ReportService.process_general_exploit(exploit)
        processed_exploit['type'] = 'weblogic'
        return processed_exploit

    @staticmethod
    def process_hadoop_exploit(exploit):
        processed_exploit = ReportService.process_general_exploit(exploit)
        processed_exploit['type'] = 'hadoop'
        return processed_exploit

    @staticmethod
    def process_exploit(exploit):
        exploiter_type = exploit['data']['exploiter']
        EXPLOIT_PROCESS_FUNCTION_DICT = {
            'SmbExploiter': ReportService.process_smb_exploit,
            'WmiExploiter': ReportService.process_wmi_exploit,
            'SSHExploiter': ReportService.process_ssh_exploit,
            'RdpExploiter': ReportService.process_rdp_exploit,
            'SambaCryExploiter': ReportService.process_sambacry_exploit,
            'ElasticGroovyExploiter': ReportService.process_elastic_exploit,
            'Ms08_067_Exploiter': ReportService.process_conficker_exploit,
            'ShellShockExploiter': ReportService.process_shellshock_exploit,
            'Struts2Exploiter': ReportService.process_struts2_exploit,
            'WebLogicExploiter': ReportService.process_weblogic_exploit,
            'HadoopExploiter': ReportService.process_hadoop_exploit
        }

        return EXPLOIT_PROCESS_FUNCTION_DICT[exploiter_type](exploit)

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
        network_info = mongo.db.telemetry.find_one(
            {'telem_type': 'system_info_collection', 'monkey_guid': monkey_guid},
            {'data.network_info.networks': 1}
        )
        if network_info is None:
            return []

        return \
            [
                ipaddress.ip_interface(text_type(network['addr'] + '/' + network['netmask'])).network
                for network in network_info['data']['network_info']['networks']
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
                    if ipaddress.ip_address(text_type(ip)) in subnet:
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
        issues = ReportService.get_exploits() + ReportService.get_tunnels() +\
                 ReportService.get_cross_segment_issues() + ReportService.get_azure_issues()
        issues_dict = {}
        for issue in issues:
            machine = issue['machine']
            if machine not in issues_dict:
                issues_dict[machine] = []
            issues_dict[machine].append(issue)
        logger.info('Issues generated for reporting')
        return issues_dict

    @staticmethod
    def get_manual_monkeys():
        return [monkey['hostname'] for monkey in mongo.db.monkey.find({}, {'hostname': 1, 'parent': 1, 'guid': 1}) if
                NodeService.get_monkey_manual_run(monkey)]

    @staticmethod
    def get_config_users():
        return ConfigService.get_config_value(['basic', 'credentials', 'exploit_user_list'], True, True)

    @staticmethod
    def get_config_passwords():
        return ConfigService.get_config_value(['basic', 'credentials', 'exploit_password_list'], True, True)

    @staticmethod
    def get_config_exploits():
        exploits_config_value = ['exploits', 'general', 'exploiter_classes']
        default_exploits = ConfigService.get_default_config(False)
        for namespace in exploits_config_value:
            default_exploits = default_exploits[namespace]
        exploits = ConfigService.get_config_value(exploits_config_value, True, True)

        if exploits == default_exploits:
            return ['default']

        return [ReportService.EXPLOIT_DISPLAY_DICT[exploit] for exploit in
                exploits]

    @staticmethod
    def get_config_ips():
        return ConfigService.get_config_value(['basic_network', 'general', 'subnet_scan_list'], True, True)

    @staticmethod
    def get_config_scan():
        return ConfigService.get_config_value(['basic_network', 'general', 'local_network_scan'], True, True)

    @staticmethod
    def get_issues_overview(issues, config_users, config_passwords):
        issues_byte_array = [False] * len(ReportService.ISSUES_DICT)

        for machine in issues:
            for issue in issues[machine]:
                if issue['type'] == 'elastic':
                    issues_byte_array[ReportService.ISSUES_DICT.ELASTIC.value] = True
                elif issue['type'] == 'sambacry':
                    issues_byte_array[ReportService.ISSUES_DICT.SAMBACRY.value] = True
                elif issue['type'] == 'shellshock':
                    issues_byte_array[ReportService.ISSUES_DICT.SHELLSHOCK.value] = True
                elif issue['type'] == 'conficker':
                    issues_byte_array[ReportService.ISSUES_DICT.CONFICKER.value] = True
                elif issue['type'] == 'azure_password':
                    issues_byte_array[ReportService.ISSUES_DICT.AZURE.value] = True
                elif issue['type'] == 'ssh_key':
                    issues_byte_array[ReportService.ISSUES_DICT.STOLEN_SSH_KEYS.value] = True
                elif issue['type'] == 'struts2':
                    issues_byte_array[ReportService.ISSUES_DICT.STRUTS2.value] = True
                elif issue['type'] == 'weblogic':
                    issues_byte_array[ReportService.ISSUES_DICT.WEBLOGIC.value] = True
                elif issue['type'] == 'hadoop':
                    issues_byte_array[ReportService.ISSUES_DICT.HADOOP.value] = True
                elif issue['type'].endswith('_password') and issue['password'] in config_passwords and \
                        issue['username'] in config_users or issue['type'] == 'ssh':
                    issues_byte_array[ReportService.ISSUES_DICT.WEAK_PASSWORD.value] = True
                elif issue['type'].endswith('_pth') or issue['type'].endswith('_password'):
                    issues_byte_array[ReportService.ISSUES_DICT.STOLEN_CREDS.value] = True

        return issues_byte_array

    @staticmethod
    def get_warnings_overview(issues):
        warnings_byte_array = [False] * 2

        for machine in issues:
            for issue in issues[machine]:
                if issue['type'] == 'cross_segment':
                    warnings_byte_array[ReportService.WARNINGS_DICT.CROSS_SEGMENT.value] = True
                elif issue['type'] == 'tunnel':
                    warnings_byte_array[ReportService.WARNINGS_DICT.TUNNEL.value] = True

        return warnings_byte_array

    @staticmethod
    def is_report_generated():
        generated_report = mongo.db.report.find_one({'name': 'generated_report'})
        if generated_report is None:
            return False
        return generated_report['value']

    @staticmethod
    def set_report_generated():
        mongo.db.report.update(
            {'name': 'generated_report'},
            {'$set': {'value': True}},
            upsert=True)
        logger.info("Report marked as generated.")

    @staticmethod
    def get_report():
        issues = ReportService.get_issues()
        config_users = ReportService.get_config_users()
        config_passwords = ReportService.get_config_passwords()

        report = \
            {
                'overview':
                    {
                        'manual_monkeys': ReportService.get_manual_monkeys(),
                        'config_users': config_users,
                        'config_passwords': config_passwords,
                        'config_exploits': ReportService.get_config_exploits(),
                        'config_ips': ReportService.get_config_ips(),
                        'config_scan': ReportService.get_config_scan(),
                        'monkey_start_time': ReportService.get_first_monkey_time().strftime("%d/%m/%Y %H:%M:%S"),
                        'monkey_duration': ReportService.get_monkey_duration(),
                        'issues': ReportService.get_issues_overview(issues, config_users, config_passwords),
                        'warnings': ReportService.get_warnings_overview(issues)
                    },
                'glance':
                    {
                        'scanned': ReportService.get_scanned(),
                        'exploited': ReportService.get_exploited(),
                        'stolen_creds': ReportService.get_stolen_creds(),
                        'azure_passwords': ReportService.get_azure_creds(),
                        'ssh_keys': ReportService.get_ssh_keys()
                    },
                'recommendations':
                    {
                        'issues': issues
                    }
            }

        finished_run = NodeService.is_monkey_finished_running()
        if finished_run:
            ReportService.set_report_generated()

        return report

    @staticmethod
    def did_exploit_type_succeed(exploit_type):
        return mongo.db.edge.count(
            {'exploits': {'$elemMatch': {'exploiter': exploit_type, 'result': True}}},
            limit=1) > 0
