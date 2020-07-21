import copy

from common.data.post_breach_consts import (
    POST_BREACH_COMMUNICATE_AS_NEW_USER,
    POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION)
from monkey_island.cc.database import mongo
from monkey_island.cc.models import Monkey
from monkey_island.cc.services.telemetry.zero_trust_tests.communicate_as_new_user import \
    test_new_user_communication


def process_communicate_as_new_user_telemetry(telemetry_json):
    current_monkey = Monkey.get_single_monkey_by_guid(telemetry_json['monkey_guid'])
    message = telemetry_json['data']['result'][0]
    success = telemetry_json['data']['result'][1]
    test_new_user_communication(current_monkey, success, message)


def process_shell_startup_file_modification_telemetry(telemetry_json):
    modified_data = []
    for result in telemetry_json['data']['result']:
        temp = copy.deepcopy(telemetry_json['data'])
        temp['result'] = result
        modified_data.append(temp)
    telemetry_json['data'] = modified_data


POST_BREACH_TELEMETRY_PROCESSING_FUNCS = {
    POST_BREACH_COMMUNICATE_AS_NEW_USER: process_communicate_as_new_user_telemetry,
    POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION: process_shell_startup_file_modification_telemetry,
}


def process_post_breach_telemetry(telemetry_json):
    post_breach_action_name = telemetry_json["data"]["name"]
    if post_breach_action_name in POST_BREACH_TELEMETRY_PROCESSING_FUNCS:
        POST_BREACH_TELEMETRY_PROCESSING_FUNCS[post_breach_action_name](telemetry_json)

    if type(telemetry_json['data']) is list:
        for pba_data in telemetry_json['data']:
            mongo.db.monkey.update(
                {'guid': telemetry_json['monkey_guid']},
                {'$push': {'pba_results': pba_data}})
    else:
        mongo.db.monkey.update(
            {'guid': telemetry_json['monkey_guid']},
            {'$push': {'pba_results': telemetry_json['data']}})
