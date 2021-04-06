from datetime import datetime

import pytest

from common.common_consts import zero_trust_consts
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.models.zero_trust.monkey_finding import MonkeyFinding
from monkey_island.cc.services.zero_trust.monkey_findings.monkey_zt_finding_service import MonkeyZTFindingService
from monkey_island.cc.test_common.fixtures import FixtureEnum

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


class TestMonkeyZTFindingService:

    @pytest.mark.usefixtures(FixtureEnum.USES_DATABASE)
    def test_create_or_add_to_existing_creation(self):
        # Create new finding
        MonkeyZTFindingService.create_or_add_to_existing(test=TESTS[0], status=STATUS[0], events=[EVENTS[0]])
        # Assert that it was properly created
        findings = list(Finding.objects())
        assert len(findings) == 1
        assert findings[0].test == TESTS[0]
        assert findings[0].status == STATUS[0]
        finding_details = findings[0].details.fetch()
        assert len(finding_details.events) == 1
        assert finding_details.events[0].message == EVENTS[0].message

    @pytest.mark.usefixtures(FixtureEnum.USES_DATABASE)
    def test_create_or_add_to_existing_addition(self):
        # Create new finding
        MonkeyZTFindingService.create_or_add_to_existing(test=TESTS[0], status=STATUS[0], events=[EVENTS[0]])
        # Assert that there's only one finding
        assert len(Finding.objects()) == 1

        # Add events to an existing finding
        MonkeyZTFindingService.create_or_add_to_existing(test=TESTS[0], status=STATUS[0], events=[EVENTS[1]])
        # Assert there's still only one finding, only events got appended
        assert len(Finding.objects()) == 1
        assert len(Finding.objects()[0].details.fetch().events) == 2

        # Create new finding
        MonkeyZTFindingService.create_or_add_to_existing(test=TESTS[1], status=STATUS[1], events=[EVENTS[1]])
        # Assert there was a new finding created, because test and status is different
        assert len(MonkeyFinding.objects()) == 2
