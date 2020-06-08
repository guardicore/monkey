import logging

from monkey_island.cc.encryptor import encryptor
from monkey_island.cc.services.config import ConfigService
from monkey_island.cc.services.node import NodeService
from monkey_island.cc.services.telemetry.processing.system_info_collectors.system_info_telemetry_dispatcher import \
    SystemInfoTelemetryDispatcher
from monkey_island.cc.services.wmi_handler import WMIHandler

logger = logging.getLogger(__name__)


def process_system_info_telemetry(telemetry_json):
    dispatcher = SystemInfoTelemetryDispatcher()
    telemetry_processing_stages = [
        process_ssh_info,
        process_credential_info,
        process_wmi_info,
        dispatcher.dispatch_collector_results_to_relevant_processors
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
            "Error {} while in {} stage of processing telemetry.".format(str(err), processing_function.__name__),
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
        add_system_info_creds_to_config(creds)
        replace_user_dot_with_comma(creds)


def replace_user_dot_with_comma(creds):
    for user in creds:
        if -1 != user.find('.'):
            new_user = user.replace('.', ',')
            creds[new_user] = creds.pop(user)


def add_system_info_creds_to_config(creds):
    for user in creds:
        ConfigService.creds_add_username(creds[user]['username'])
        if 'password' in creds[user] and creds[user]['password']:
            ConfigService.creds_add_password(creds[user]['password'])
        if 'lm_hash' in creds[user] and creds[user]['lm_hash']:
            ConfigService.creds_add_lm_hash(creds[user]['lm_hash'])
        if 'ntlm_hash' in creds[user] and creds[user]['ntlm_hash']:
            ConfigService.creds_add_ntlm_hash(creds[user]['ntlm_hash'])


def process_wmi_info(telemetry_json):
    users_secrets = {}

    if 'wmi' in telemetry_json['data']:
        monkey_id = NodeService.get_monkey_by_guid(telemetry_json['monkey_guid']).get('_id')
        wmi_handler = WMIHandler(monkey_id, telemetry_json['data']['wmi'], users_secrets)
        wmi_handler.process_and_handle_wmi_info()
