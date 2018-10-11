import json
import traceback
import logging
import copy
from datetime import datetime

import dateutil
import flask_restful
from flask import request

from cc.auth import jwt_required
from cc.database import mongo
from cc.services import user_info, group_info
from cc.services.config import ConfigService
from cc.services.edge import EdgeService
from cc.services.node import NodeService
from cc.encryptor import encryptor

__author__ = 'Barak'


logger = logging.getLogger(__name__)


class Telemetry(flask_restful.Resource):
    @jwt_required()
    def get(self, **kw):
        monkey_guid = request.args.get('monkey_guid')
        telem_type = request.args.get('telem_type')
        timestamp = request.args.get('timestamp')
        if "null" == timestamp:  # special case to avoid ugly JS code...
            timestamp = None

        result = {'timestamp': datetime.now().isoformat()}
        find_filter = {}

        if monkey_guid:
            find_filter["monkey_guid"] = {'$eq': monkey_guid}
        if telem_type:
            find_filter["telem_type"] = {'$eq': telem_type}
        if timestamp:
            find_filter['timestamp'] = {'$gt': dateutil.parser.parse(timestamp)}

        result['objects'] = self.telemetry_to_displayed_telemetry(mongo.db.telemetry.find(find_filter))
        return result

    # Used by monkey. can't secure.
    def post(self):
        telemetry_json = json.loads(request.data)
        telemetry_json['timestamp'] = datetime.now()

        monkey = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])

        try:
            NodeService.update_monkey_modify_time(monkey["_id"])
            telem_type = telemetry_json.get('telem_type')
            if telem_type in TELEM_PROCESS_DICT:
                TELEM_PROCESS_DICT[telem_type](telemetry_json)
            else:
                logger.info('Got unknown type of telemetry: %s' % telem_type)
        except Exception as ex:
            logger.error("Exception caught while processing telemetry", exc_info=True)

        telem_id = mongo.db.telemetry.insert(telemetry_json)
        return mongo.db.telemetry.find_one_or_404({"_id": telem_id})

    @staticmethod
    def telemetry_to_displayed_telemetry(telemetry):
        monkey_guid_dict = {}
        monkeys = mongo.db.monkey.find({})
        for monkey in monkeys:
            monkey_guid_dict[monkey["guid"]] = NodeService.get_monkey_label(monkey)

        objects = []
        for x in telemetry:
            telem_monkey_guid = x.pop("monkey_guid")
            monkey_label = monkey_guid_dict.get(telem_monkey_guid)
            if monkey_label is None:
                monkey_label = telem_monkey_guid
            x["monkey"] = monkey_label
            objects.append(x)
            if x['telem_type'] == 'system_info_collection' and 'credentials' in x['data']:
                for user in x['data']['credentials']:
                    if -1 != user.find(','):
                        new_user = user.replace(',', '.')
                        x['data']['credentials'][new_user] = x['data']['credentials'].pop(user)

        return objects

    @staticmethod
    def get_edge_by_scan_or_exploit_telemetry(telemetry_json):
        dst_ip = telemetry_json['data']['machine']['ip_addr']
        src_monkey = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])
        dst_node = NodeService.get_monkey_by_ip(dst_ip)
        if dst_node is None:
            dst_node = NodeService.get_or_create_node(dst_ip)

        return EdgeService.get_or_create_edge(src_monkey["_id"], dst_node["_id"])

    @staticmethod
    def process_tunnel_telemetry(telemetry_json):
        monkey_id = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])["_id"]
        if telemetry_json['data']['proxy'] is not None:
            tunnel_host_ip = telemetry_json['data']['proxy'].split(":")[-2].replace("//", "")
            NodeService.set_monkey_tunnel(monkey_id, tunnel_host_ip)
        else:
            NodeService.unset_all_monkey_tunnels(monkey_id)

    @staticmethod
    def process_state_telemetry(telemetry_json):
        monkey = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])
        if telemetry_json['data']['done']:
            NodeService.set_monkey_dead(monkey, True)
        else:
            NodeService.set_monkey_dead(monkey, False)

    @staticmethod
    def process_exploit_telemetry(telemetry_json):
        edge = Telemetry.get_edge_by_scan_or_exploit_telemetry(telemetry_json)
        Telemetry.encrypt_exploit_creds(telemetry_json)

        new_exploit = copy.deepcopy(telemetry_json['data'])

        new_exploit.pop('machine')
        new_exploit['timestamp'] = telemetry_json['timestamp']

        mongo.db.edge.update(
            {'_id': edge['_id']},
            {'$push': {'exploits': new_exploit}}
        )
        if new_exploit['result']:
            EdgeService.set_edge_exploited(edge)

        for attempt in telemetry_json['data']['attempts']:
            if attempt['result']:
                found_creds = {'user': attempt['user']}
                for field in ['password', 'lm_hash', 'ntlm_hash', 'ssh_key']:
                    if len(attempt[field]) != 0:
                        found_creds[field] = attempt[field]
                NodeService.add_credentials_to_node(edge['to'], found_creds)

    @staticmethod
    def process_scan_telemetry(telemetry_json):
        edge = Telemetry.get_edge_by_scan_or_exploit_telemetry(telemetry_json)
        data = copy.deepcopy(telemetry_json['data']['machine'])
        ip_address = data.pop("ip_addr")
        new_scan = \
            {
                "timestamp": telemetry_json["timestamp"],
                "data": data,
                "scanner": telemetry_json['data']['scanner']
            }
        mongo.db.edge.update(
            {"_id": edge["_id"]},
            {"$push": {"scans": new_scan},
             "$set": {"ip_address": ip_address}}
        )

        node = mongo.db.node.find_one({"_id": edge["to"]})
        if node is not None:
            if new_scan["scanner"] == "TcpScanner":
                scan_os = new_scan["data"]["os"]
                if "type" in scan_os:
                    mongo.db.node.update({"_id": node["_id"]},
                                         {"$set": {"os.type": scan_os["type"]}},
                                         upsert=False)
                if "version" in scan_os:
                    mongo.db.node.update({"_id": node["_id"]},
                                         {"$set": {"os.version": scan_os["version"]}},
                                         upsert=False)

    @staticmethod
    def process_system_info_telemetry(telemetry_json):
        users_secrets = {}
        monkey_id = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid']).get('_id')
        if 'ssh_info' in telemetry_json['data']:
            ssh_info = telemetry_json['data']['ssh_info']
            Telemetry.encrypt_system_info_ssh_keys(ssh_info)
            if telemetry_json['data']['network_info']['networks']:
                # We use user_name@machine_ip as the name of the ssh key stolen, thats why we need ip from telemetry
                Telemetry.add_ip_to_ssh_keys(telemetry_json['data']['network_info']['networks'][0], ssh_info)
            Telemetry.add_system_info_ssh_keys_to_config(ssh_info)
        if 'credentials' in telemetry_json['data']:
            creds = telemetry_json['data']['credentials']
            Telemetry.encrypt_system_info_creds(creds)
            Telemetry.add_system_info_creds_to_config(creds)
            Telemetry.replace_user_dot_with_comma(creds)
        if 'mimikatz' in telemetry_json['data']:
            users_secrets = user_info.extract_secrets_from_mimikatz(telemetry_json['data'].get('mimikatz', ''))
        if 'wmi' in telemetry_json['data']:
            info_for_mongo = {}
            users_info = telemetry_json['data']['wmi']['Win32_UserAccount']
            groups_info = telemetry_json['data']['wmi']['Win32_Group']
            group_user_dict = telemetry_json['data']['wmi']['Win32_GroupUser']
            Telemetry.add_groups_to_collection(groups_info, info_for_mongo, monkey_id)
            Telemetry.add_users_to_collection(users_info, info_for_mongo, users_secrets, monkey_id)
            Telemetry.create_group_user_connection(info_for_mongo, group_user_dict)
            for entity in info_for_mongo.values():
                if entity['machine_id']:
                    mongo.db.groupsandusers.update({'SID': entity['SID'],
                                                    'machine_id': entity['machine_id']}, entity, upsert=True)
                else:
                    if not mongo.db.groupsandusers.find_one({'SID': entity['SID']}):
                        mongo.db.groupsandusers.insert_one(entity)

            Telemetry.add_admin(info_for_mongo[group_info.ADMINISTRATORS_GROUP_KNOWN_SID], monkey_id)
            Telemetry.update_admins_retrospective(info_for_mongo)
            Telemetry.update_critical_services(telemetry_json['data']['wmi']['Win32_Service'],
                                               telemetry_json['data']['wmi']['Win32_Product'],
                                               monkey_id)

    @staticmethod
    def update_critical_services(wmi_services, wmi_products, machine_id):
        critical_names = ("W3svc", "MSExchangeServiceHost", "MSSQLServer", "dns", 'MSSQL$SQLEXPRESS', 'SQL')

        services_names_list = [str(i['Name'])[2:-1] for i in wmi_services]
        products_names_list = [str(i['Name'])[2:-2] for i in wmi_products]

        for name in critical_names:
            if name in services_names_list or name in products_names_list:
                logger.info('found a critical service')
                mongo.db.monkey.update({'_id': machine_id}, {'$addToSet': {'critical_services': name}})

    @staticmethod
    def update_admins_retrospective(info_for_mongo):
        for profile in info_for_mongo:
            groups_from_mongo = mongo.db.groupsandusers.find({'SID': {'$in': info_for_mongo[profile]['member_of']}},
                                                             {'admin_on_machines': 1})
            for group in groups_from_mongo:
                if group['admin_on_machines']:
                    mongo.db.groupsandusers.update_one({'SID': info_for_mongo[profile]['SID']},
                                                       {'$addToSet': {'admin_on_machines': {
                                                           '$each': group['admin_on_machines']}}})

    @staticmethod
    def add_admin(group, machine_id):
        for sid in group['entities_list']:
            mongo.db.groupsandusers.update_one({'SID': sid},
                                               {'$addToSet': {'admin_on_machines': machine_id}})
            entity_details = mongo.db.groupsandusers.find_one({'SID': sid},
                                                              {'type': 1, 'entities_list': 1})
            if entity_details.get('type') == 2:
                Telemetry.add_admin(entity_details, machine_id)

    @staticmethod
    def add_groups_to_collection(groups_info, info_for_mongo, monkey_id):
        for group in groups_info:
            if not group.get('LocalAccount'):
                base_entity = Telemetry.build_entity_document(group)
            else:
                base_entity = Telemetry.build_entity_document(group, monkey_id)
            base_entity['entities_list'] = []
            base_entity['type'] = 2
            info_for_mongo[base_entity.get('SID')] = base_entity

    @staticmethod
    def add_users_to_collection(users_info, info_for_mongo, users_secrets, monkey_id):
        for user in users_info:
            if not user.get('LocalAccount'):
                base_entity = Telemetry.build_entity_document(user)
            else:
                base_entity = Telemetry.build_entity_document(user, monkey_id)
            base_entity['NTLM_secret'] = users_secrets.get(base_entity['name'], {}).get('ntlm')
            base_entity['SAM_secret'] = users_secrets.get(base_entity['name'], {}).get('sam')
            base_entity['secret_location'] = []

            base_entity['type'] = 1
            info_for_mongo[base_entity.get('SID')] = base_entity

    @staticmethod
    def build_entity_document(entity_info, monkey_id=None):
        general_properties_dict = {
            'SID': str(entity_info['SID'])[4:-1],
            'name': str(entity_info['Name'])[2:-1],
            'machine_id': monkey_id,
            'member_of': [],
            'admin_on_machines': []
        }

        if monkey_id:
            general_properties_dict['domain_name'] = None
        else:
            general_properties_dict['domain_name'] = str(entity_info['Domain'])[2:-1]

        return general_properties_dict

    @staticmethod
    def create_group_user_connection(info_for_mongo, group_user_list):
        for group_user_couple in group_user_list:
            group_part = group_user_couple['GroupComponent']
            child_part = group_user_couple['PartComponent']
            group_sid = str(group_part['SID'])[4:-1]
            groups_entities_list = info_for_mongo[group_sid]['entities_list']
            child_sid = ''

            if type(child_part) in (unicode, str):
                child_part = str(child_part)
                if "cimv2:Win32_UserAccount" in child_part:
                    # domain user
                    domain_name = child_part.split('cimv2:Win32_UserAccount.Domain="')[1].split('",Name="')[0]
                    name = child_part.split('cimv2:Win32_UserAccount.Domain="')[1].split('",Name="')[1][:-2]

                if "cimv2:Win32_Group" in child_part:
                    # domain group
                    domain_name = child_part.split('cimv2:Win32_Group.Domain="')[1].split('",Name="')[0]
                    name = child_part.split('cimv2:Win32_Group.Domain="')[1].split('",Name="')[1][:-2]

                    for entity in info_for_mongo:
                        if info_for_mongo[entity]['name'] == name and info_for_mongo[entity]['domain'] == domain_name:
                            child_sid = info_for_mongo[entity]['SID']
            else:
                child_sid = str(child_part['SID'])[4:-1]

            if child_sid and child_sid not in groups_entities_list:
                groups_entities_list.append(child_sid)

            if child_sid: #and info_for_mongo.get(child_sid, {}).get('type') == 1:
                if child_sid in info_for_mongo:
                    info_for_mongo[child_sid]['member_of'].append(group_sid)


################################################################


    @staticmethod
    def add_ip_to_ssh_keys(ip, ssh_info):
        for key in ssh_info:
            key['ip'] = ip['addr']

    @staticmethod
    def process_trace_telemetry(telemetry_json):
        # Nothing to do
        return

    @staticmethod
    def replace_user_dot_with_comma(creds):
        for user in creds:
            if -1 != user.find('.'):
                new_user = user.replace('.', ',')
                creds[new_user] = creds.pop(user)

    @staticmethod
    def encrypt_system_info_creds(creds):
        for user in creds:
            for field in ['password', 'lm_hash', 'ntlm_hash']:
                if field in creds[user]:
                    # this encoding is because we might run into passwords which are not pure ASCII
                    creds[user][field] = encryptor.enc(creds[user][field].encode('utf-8'))

    @staticmethod
    def encrypt_system_info_ssh_keys(ssh_info):
        for idx, user in enumerate(ssh_info):
            for field in ['public_key', 'private_key', 'known_hosts']:
                if ssh_info[idx][field]:
                    ssh_info[idx][field] = encryptor.enc(ssh_info[idx][field].encode('utf-8'))

    @staticmethod
    def add_system_info_creds_to_config(creds):
        for user in creds:
            ConfigService.creds_add_username(user)
            if 'password' in creds[user]:
                ConfigService.creds_add_password(creds[user]['password'])
            if 'lm_hash' in creds[user]:
                ConfigService.creds_add_lm_hash(creds[user]['lm_hash'])
            if 'ntlm_hash' in creds[user]:
                ConfigService.creds_add_ntlm_hash(creds[user]['ntlm_hash'])

    @staticmethod
    def add_system_info_ssh_keys_to_config(ssh_info):
        for user in ssh_info:
            ConfigService.creds_add_username(user['name'])
            # Public key is useless without private key
            if user['public_key'] and user['private_key']:
                ConfigService.ssh_add_keys(user['public_key'], user['private_key'],
                                           user['name'], user['ip'])

    @staticmethod
    def encrypt_exploit_creds(telemetry_json):
        attempts = telemetry_json['data']['attempts']
        for i in range(len(attempts)):
            for field in ['password', 'lm_hash', 'ntlm_hash']:
                credential = attempts[i][field]
                if len(credential) > 0:
                    attempts[i][field] = encryptor.enc(credential.encode('utf-8'))


TELEM_PROCESS_DICT = \
    {
        'tunnel': Telemetry.process_tunnel_telemetry,
        'state': Telemetry.process_state_telemetry,
        'exploit': Telemetry.process_exploit_telemetry,
        'scan': Telemetry.process_scan_telemetry,
        'system_info_collection': Telemetry.process_system_info_telemetry,
        'trace': Telemetry.process_trace_telemetry
    }
