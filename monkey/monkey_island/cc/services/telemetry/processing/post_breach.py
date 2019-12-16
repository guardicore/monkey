from common.data.post_breach_consts import POST_BREACH_COMMUNICATE_AS_NEW_USER
from monkey_island.cc.database import mongo
from monkey_island.cc.models import Monkey
from monkey_island.cc.services.telemetry.zero_trust_tests.communicate_as_new_user import test_new_user_communication


def process_communicate_as_new_user_telemetry(telemetry_json):
    current_monkey = Monkey.get_single_monkey_by_guid(telemetry_json['monkey_guid'])
    message = telemetry_json['data']['result'][0]
    success = telemetry_json['data']['result'][1]
    test_new_user_communication(current_monkey, success, message)


POST_BREACH_TELEMETRY_PROCESSING_FUNCS = {
    POST_BREACH_COMMUNICATE_AS_NEW_USER: process_communicate_as_new_user_telemetry,
}


def process_post_breach_telemetry(telemetry_json):
    mongo.db.monkey.update(
        {'guid': telemetry_json['monkey_guid']},
        {'$push': {'pba_results': telemetry_json['data']}})

    post_breach_action_name = telemetry_json["data"]["name"]
    if post_breach_action_name in POST_BREACH_TELEMETRY_PROCESSING_FUNCS:
        POST_BREACH_TELEMETRY_PROCESSING_FUNCS[post_breach_action_name](telemetry_json)
