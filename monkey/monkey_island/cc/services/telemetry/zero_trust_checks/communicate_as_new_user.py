import common.common_consts.zero_trust_consts as zero_trust_consts
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.services.zero_trust.monkey_finding_service import MonkeyFindingService

COMM_AS_NEW_USER_FAILED_FORMAT = "Monkey on {} couldn't communicate as new user. Details: {}"
COMM_AS_NEW_USER_SUCCEEDED_FORMAT = \
    "New user created by Monkey on {} successfully tried to communicate with the internet. Details: {}"


def check_new_user_communication(current_monkey, success, message):
    MonkeyFindingService.create_or_add_to_existing(test=zero_trust_consts.TEST_COMMUNICATE_AS_NEW_USER,
                                                   status=zero_trust_consts.STATUS_FAILED if success else zero_trust_consts.STATUS_PASSED,
                                                   events=[
                                                       get_attempt_event(current_monkey),
                                                       get_result_event(current_monkey, message, success)
                                                   ])


def get_attempt_event(current_monkey):
    tried_to_communicate_event = Event.create_event(
        title="Communicate as new user",
        message="Monkey on {} tried to create a new user and communicate from it.".format(current_monkey.hostname),
        event_type=zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK)
    return tried_to_communicate_event


def get_result_event(current_monkey, message, success):
    message_format = COMM_AS_NEW_USER_SUCCEEDED_FORMAT if success else COMM_AS_NEW_USER_FAILED_FORMAT

    return Event.create_event(
        title="Communicate as new user",
        message=message_format.format(current_monkey.hostname, message),
        event_type=zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK)
