from common.data.zero_trust_consts import EVENT_TYPE_MONKEY_NETWORK, STATUS_FAILED, TEST_COMMUNICATE_AS_NEW_USER, \
    STATUS_PASSED
from monkey_island.cc.models.zero_trust.aggregate_finding import AggregateFinding
from monkey_island.cc.models.zero_trust.event import Event


def test_new_user_communication(current_monkey, success, message):
    tried_to_communicate_event = Event.create_event(
        title="Communicate as new user",
        message="Monkey on {} tried to create a new user and communicate from it.".format(current_monkey.hostname),
        event_type=EVENT_TYPE_MONKEY_NETWORK)
    events = [tried_to_communicate_event]

    if success:
        events.append(
            Event.create_event(
                title="Communicate as new user",
                message="New user created by Monkey on {} successfully tried to communicate with the internet. "
                        "Details: {}".format(current_monkey.hostname, message),
                event_type=EVENT_TYPE_MONKEY_NETWORK)
        )
        test_status = STATUS_FAILED
    else:
        events.append(
            Event.create_event(
                title="Communicate as new user",
                message="Monkey on {} couldn't communicate as new user. Details: {}".format(
                    current_monkey.hostname, message),
                event_type=EVENT_TYPE_MONKEY_NETWORK)
        )
        test_status = STATUS_PASSED

    AggregateFinding.create_or_add_to_existing(
        test=TEST_COMMUNICATE_AS_NEW_USER, status=test_status, events=events
    )
