import json
import logging
import copy
from datetime import datetime

import dateutil
import flask_restful
from flask import request

from monkey_island.cc.auth import jwt_required
from monkey_island.cc.database import mongo
from monkey_island.cc.services import mimikatz_utils
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.edge import EdgeService
from monkey_island.cc.services.node import NodeService
from monkey_island.cc.encryptor import encryptor
from monkey_island.cc.services.wmi_handler import WMIHandler

__author__ = 'Barak'


logger = logging.getLogger(__name__)


class Telemetry(flask_restful.Resource):
    @jwt_required()
    def get(self, **kw):
        monkey_guid = request.args.get('monkey_guid')
        telem_catagory = request.args.get('telem_catagory')
        timestamp = request.args.get('timestamp')
        if "null" == timestamp:  # special case to avoid ugly JS code...
            timestamp = None

        result = {'timestamp': datetime.now().isoformat()}
        find_filter = {}

        if monkey_guid:
            find_filter["monkey_guid"] = {'$eq': monkey_guid}
        if telem_catagory:
            find_filter["telem_catagory"] = {'$eq': telem_catagory}
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
            telem_catagory = telemetry_json.get('telem_catagory')
            if telem_catagory in TELEM_PROCESS_DICT:
                TELEM_PROCESS_DICT[telem_catagory](telemetry_json)
            else:
                logger.info('Got unknown type of telemetry: %s' % telem_catagory)
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
            if x['telem_catagory'] == 'system_info_collection' and 'credentials' in x['data']:
                for user in x['data']['credentials']:
                    if -1 != user.find(','):
                        new_user = user.replace(',', '.')
                        x['data']['credentials'][new_user] = x['data']['credentials'].pop(user)

        return objects

    @staticmethod
    def get_edge_by_scan_or_exploit_telemetry(telemetry_json):
        dst_ip = telemetry_json['data']['machine']['ip_addr']
        dst_domain_name = telemetry_json['data']['machine']['domain_name']
        src_monkey = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid'])
        dst_node = NodeService.get_monkey_by_ip(dst_ip)
        if dst_node is None:
            dst_node = NodeService.get_or_create_node(dst_ip, dst_domain_name)

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
        telemetry_json['data']['info']['started'] = dateutil.parser.parse(telemetry_json['data']['info']['started'])
        telemetry_json['data']['info']['finished'] = dateutil.parser.parse(telemetry_json['data']['info']['finished'])

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
        domain_name = data.pop("domain_name")
        new_scan = \
            {
                "timestamp": telemetry_json["timestamp"],
                "data": data
            }
        mongo.db.edge.update(
            {"_id": edge["_id"]},
            {"$push": {"scans": new_scan},
             "$set": {"ip_address": ip_address, 'domain_name': domain_name}}
        )

        node = mongo.db.node.find_one({"_id": edge["to"]})
        if node is not None:
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
            users_secrets = mimikatz_utils.MimikatzSecrets.\
                extract_secrets_from_mimikatz(telemetry_json['data'].get('mimikatz', ''))
        if 'wmi' in telemetry_json['data']:
            wmi_handler = WMIHandler(monkey_id, telemetry_json['data']['wmi'], users_secrets)
            wmi_handler.process_and_handle_wmi_info()
        if 'aws' in telemetry_json['data']:
            if 'instance_id' in telemetry_json['data']['aws']:
                mongo.db.monkey.update_one({'_id': monkey_id},
                                           {'$set': {'aws_instance_id': telemetry_json['data']['aws']['instance_id']}})

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

    @staticmethod
    def process_post_breach_telemetry(telemetry_json):
        mongo.db.monkey.update(
            {'guid': telemetry_json['monkey_guid']},
            {'$push': {'pba_results': telemetry_json['data']}})

    @staticmethod
    def process_attack_telemetry(telemetry_json):
        # No processing required
        pass


TELEM_PROCESS_DICT = \
    {
        'tunnel': Telemetry.process_tunnel_telemetry,
        'state': Telemetry.process_state_telemetry,
        'exploit': Telemetry.process_exploit_telemetry,
        'scan': Telemetry.process_scan_telemetry,
        'system_info_collection': Telemetry.process_system_info_telemetry,
        'trace': Telemetry.process_trace_telemetry,
        'post_breach': Telemetry.process_post_breach_telemetry,
        'attack': Telemetry.process_attack_telemetry
    }
