import copy

from common.data.post_breach_consts import (
    POST_BREACH_COMMUNICATE_AS_NEW_USER,
    POST_BREACH_SHELL_STARTUP_FILE_MODIFICATION)
from monkey_island.cc.database import mongo
from monkey_island.cc.models import Monkey
from monkey_island.cc.services.telemetry.zero_trust_tests.communicate_as_new_user import \
    test_new_user_communication

EXECUTION_WITHOUT_OUTPUT = "(PBA execution produced no output)"


def process_communicate_as_new_user_telemetry(telemetry_json):
    current_monkey = Monkey.get_single_monkey_by_guid(telemetry_json['monkey_guid'])
    message = telemetry_json['data']['result'][0]
    success = telemetry_json['data']['result'][1]
    test_new_user_communication(current_monkey, success, message)


def modify_data(telemetry_json):
    modified_data = [telemetry_json['data']]
    if type(telemetry_json['data']['result'][0]) is list:
        modified_data = []
        for result in telemetry_json['data']['result']:
            temp = copy.deepcopy(telemetry_json['data'])
            temp['result'] = result
            modified_data.append(temp)
    telemetry_json['data'] = modified_data


POST_BREACH_TELEMETRY_PROCESSING_FUNCS = {
    POST_BREACH_COMMUNICATE_AS_NEW_USER: process_communicate_as_new_user_telemetry,
}


def process_post_breach_telemetry(telemetry_json):
    def modify_blank_outputs(data):
        if not data['result'][0]:
            data['result'][0] = EXECUTION_WITHOUT_OUTPUT

    def update_data(data):
        modify_blank_outputs(data)
        mongo.db.monkey.update(
            {'guid': telemetry_json['monkey_guid']},
            {'$push': {'pba_results': data}})

    post_breach_action_name = telemetry_json["data"]["name"]
    if post_breach_action_name in POST_BREACH_TELEMETRY_PROCESSING_FUNCS:
        POST_BREACH_TELEMETRY_PROCESSING_FUNCS[post_breach_action_name](telemetry_json)

    modify_data(telemetry_json)

    for pba_data in telemetry_json['data']:
        update_data(pba_data)
