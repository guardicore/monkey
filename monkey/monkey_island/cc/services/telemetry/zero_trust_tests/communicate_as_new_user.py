from common.data.zero_trust_consts import EVENT_TYPE_MONKEY_NETWORK, STATUS_FAILED, TEST_COMMUNICATE_AS_NEW_USER, \
    STATUS_PASSED
from monkey_island.cc.models.zero_trust.aggregate_finding import AggregateFinding
from monkey_island.cc.models.zero_trust.event import Event

COMM_AS_NEW_USER_FAILED_FORMAT = "Monkey on {} couldn't communicate as new user. Details: {}"
COMM_AS_NEW_USER_SUCCEEDED_FORMAT = \
    "New user created by Monkey on {} successfully tried to communicate with the internet. Details: {}"


def test_new_user_communication(current_monkey, success, message):
    AggregateFinding.create_or_add_to_existing(
        test=TEST_COMMUNICATE_AS_NEW_USER,
        status=STATUS_PASSED if success else STATUS_FAILED,
        events=[
            get_attempt_event(current_monkey),
            get_result_event(current_monkey, message, success)
        ]
    )


def get_attempt_event(current_monkey):
    tried_to_communicate_event = Event.create_event(
        title="Communicate as new user",
        message="Monkey on {} tried to create a new user and communicate from it.".format(current_monkey.hostname),
        event_type=EVENT_TYPE_MONKEY_NETWORK)
    return tried_to_communicate_event


def get_result_event(current_monkey, message, success):
    message_format = COMM_AS_NEW_USER_SUCCEEDED_FORMAT if success else COMM_AS_NEW_USER_FAILED_FORMAT

    return Event.create_event(
        title="Communicate as new user",
        message=message_format.format(current_monkey.hostname, message),
        event_type=EVENT_TYPE_MONKEY_NETWORK)
