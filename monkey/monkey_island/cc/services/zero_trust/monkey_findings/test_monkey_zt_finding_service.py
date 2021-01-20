from datetime import datetime
from typing import List

from bson import ObjectId

from common.common_consts import zero_trust_consts
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.models.zero_trust.monkey_finding_details import MonkeyFindingDetails
from monkey_island.cc.services.zero_trust.monkey_findings.monkey_zt_finding_service import MonkeyZTFindingService
from monkey_island.cc.testing.IslandTestCase import IslandTestCase

EVENTS = [
    Event.create_event(
        title='Process list',
        message='Monkey on gc-pc-244 scanned the process list',
        event_type='monkey_local',
        timestamp=datetime.strptime('2021-01-19 12:07:17.802138', '%Y-%m-%d %H:%M:%S.%f')
    ),
    Event.create_event(
        title='Communicate as new user',
        message='Monkey on gc-pc-244 couldn\'t communicate as new user. '
                'Details: System error 5 has occurred. Access is denied.',
        event_type='monkey_network',
        timestamp=datetime.strptime('2021-01-19 12:22:42.246020', '%Y-%m-%d %H:%M:%S.%f')
    )
]

TESTS = [
    zero_trust_consts.TEST_ENDPOINT_SECURITY_EXISTS,
    zero_trust_consts.TEST_COMMUNICATE_AS_NEW_USER
]

STATUS = [
    zero_trust_consts.STATUS_PASSED,
    zero_trust_consts.STATUS_FAILED,
    zero_trust_consts.STATUS_VERIFY
]


class TestMonkeyZTFindingService(IslandTestCase):

    def test_create_or_add_to_existing(self):

        # Create new finding
        MonkeyZTFindingService.create_or_add_to_existing(test=TESTS[0], status=STATUS[0], events=EVENTS[0])

        # Add events to an existing finding
        MonkeyZTFindingService.create_or_add_to_existing(test=TESTS[0], status=STATUS[0], events=EVENTS[1])

        # Create new finding
        MonkeyZTFindingService.create_or_add_to_existing(test=TESTS[1], status=STATUS[1], events=EVENTS[1])
