import logging

from monkey_island.cc.database import mongo
from monkey_island.cc.models import Monkey
from monkey_island.cc.services import mimikatz_utils
from monkey_island.cc.services.node import NodeService
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.telemetry.zero_trust_tests.antivirus_existence import test_antivirus_existence
from monkey_island.cc.services.wmi_handler import WMIHandler
from monkey_island.cc.encryptor import encryptor

logger = logging.getLogger(__name__)


def process_system_info_telemetry(telemetry_json):
    telemetry_processing_stages = [
        process_ssh_info,
        process_credential_info,
        process_mimikatz_and_wmi_info,
        process_aws_data,
        update_db_with_new_hostname,
        test_antivirus_existence,
    ]

    # Calling safe_process_telemetry so if one of the stages fail, we log and move on instead of failing the rest of
    # them, as they are independent.
    for stage in telemetry_processing_stages:
        safe_process_telemetry(stage, telemetry_json)


def safe_process_telemetry(processing_function, telemetry_json):
    # noinspection PyBroadException
    try:
        processing_function(telemetry_json)
    except Exception as err:
        logger.error(
            "Error {} while in {} stage of processing telemetry.".format(str(err), processing_function.func_name),
            exc_info=True)


def process_ssh_info(telemetry_json):
    if 'ssh_info' in telemetry_json['data']:
        ssh_info = telemetry_json['data']['ssh_info']
        encrypt_system_info_ssh_keys(ssh_info)
        if telemetry_json['data']['network_info']['networks']:
            # We use user_name@machine_ip as the name of the ssh key stolen, thats why we need ip from telemetry
            add_ip_to_ssh_keys(telemetry_json['data']['network_info']['networks'][0], ssh_info)
        add_system_info_ssh_keys_to_config(ssh_info)


def add_system_info_ssh_keys_to_config(ssh_info):
    for user in ssh_info:
        ConfigService.creds_add_username(user['name'])
        # Public key is useless without private key
        if user['public_key'] and user['private_key']:
            ConfigService.ssh_add_keys(user['public_key'], user['private_key'],
                                       user['name'], user['ip'])


def add_ip_to_ssh_keys(ip, ssh_info):
    for key in ssh_info:
        key['ip'] = ip['addr']


def encrypt_system_info_ssh_keys(ssh_info):
    for idx, user in enumerate(ssh_info):
        for field in ['public_key', 'private_key', 'known_hosts']:
            if ssh_info[idx][field]:
                ssh_info[idx][field] = encryptor.enc(ssh_info[idx][field])


def process_credential_info(telemetry_json):
    if 'credentials' in telemetry_json['data']:
        creds = telemetry_json['data']['credentials']
        encrypt_system_info_creds(creds)
        add_system_info_creds_to_config(creds)
        replace_user_dot_with_comma(creds)


def replace_user_dot_with_comma(creds):
    for user in creds:
        if -1 != user.find('.'):
            new_user = user.replace('.', ',')
            creds[new_user] = creds.pop(user)


def add_system_info_creds_to_config(creds):
    for user in creds:
        ConfigService.creds_add_username(user)
        if 'password' in creds[user]:
            ConfigService.creds_add_password(creds[user]['password'])
        if 'lm_hash' in creds[user]:
            ConfigService.creds_add_lm_hash(creds[user]['lm_hash'])
        if 'ntlm_hash' in creds[user]:
            ConfigService.creds_add_ntlm_hash(creds[user]['ntlm_hash'])


def encrypt_system_info_creds(creds):
    for user in creds:
        for field in ['password', 'lm_hash', 'ntlm_hash']:
            if field in creds[user]:
                # this encoding is because we might run into passwords which are not pure ASCII
                creds[user][field] = encryptor.enc(creds[user][field])


def process_mimikatz_and_wmi_info(telemetry_json):
    users_secrets = {}
    if 'mimikatz' in telemetry_json['data']:
        users_secrets = mimikatz_utils.MimikatzSecrets. \
            extract_secrets_from_mimikatz(telemetry_json['data'].get('mimikatz', ''))
    if 'wmi' in telemetry_json['data']:
        monkey_id = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid']).get('_id')
        wmi_handler = WMIHandler(monkey_id, telemetry_json['data']['wmi'], users_secrets)
        wmi_handler.process_and_handle_wmi_info()


def process_aws_data(telemetry_json):
    if 'aws' in telemetry_json['data']:
        if 'instance_id' in telemetry_json['data']['aws']:
            monkey_id = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid']).get('_id')
            mongo.db.monkey.update_one({'_id': monkey_id},
                                       {'$set': {'aws_instance_id': telemetry_json['data']['aws']['instance_id']}})


def update_db_with_new_hostname(telemetry_json):
    Monkey.get_single_monkey_by_guid(telemetry_json['monkey_guid']).set_hostname(telemetry_json['data']['hostname'])
