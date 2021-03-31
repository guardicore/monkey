import uuid

import common.common_consts.zero_trust_consts as zero_trust_consts
from monkey_island.cc.models import Monkey
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.finding import Finding
from monkey_island.cc.services.telemetry.zero_trust_checks.segmentation import create_or_add_findings_for_all_pairs
from monkey_island.cc.services.zero_trust.monkey_findings.monkey_zt_finding_service import MonkeyZTFindingService

FIRST_SUBNET = "1.1.1.1"
SECOND_SUBNET = "2.2.2.0/24"
THIRD_SUBNET = "3.3.3.3-3.3.3.200"


class TestSegmentationChecks:

    def test_create_findings_for_all_done_pairs(self):
        all_subnets = [FIRST_SUBNET, SECOND_SUBNET, THIRD_SUBNET]

        monkey = Monkey(
            guid=str(uuid.uuid4()),
            ip_addresses=[FIRST_SUBNET])

        # no findings
        assert len(Finding.objects(test=zero_trust_consts.TEST_SEGMENTATION)) == 0

        # This is like the monkey is done and sent done telem
        create_or_add_findings_for_all_pairs(all_subnets, monkey)

        # There are 2 subnets in which the monkey is NOT
        zt_seg_findings = Finding.objects(test=zero_trust_consts.TEST_SEGMENTATION,
                                          status=zero_trust_consts.STATUS_PASSED)

        # Assert that there's only one finding with multiple events (one for each subnet)
        assert len(zt_seg_findings) == 1
        assert len(Finding.objects().get().details.fetch().events) == 2

        # This is a monkey from 2nd subnet communicated with 1st subnet.
        MonkeyZTFindingService.create_or_add_to_existing(
            status=zero_trust_consts.STATUS_FAILED,
            test=zero_trust_consts.TEST_SEGMENTATION,
            events=[Event.create_event(title="sdf",
                                       message="asd",
                                       event_type=zero_trust_consts.EVENT_TYPE_MONKEY_NETWORK)]
        )

        zt_seg_findings = Finding.objects(test=zero_trust_consts.TEST_SEGMENTATION,
                                          status=zero_trust_consts.STATUS_PASSED)
        assert len(zt_seg_findings) == 1

        zt_seg_findings = Finding.objects(test=zero_trust_consts.TEST_SEGMENTATION,
                                          status=zero_trust_consts.STATUS_FAILED)
        assert len(zt_seg_findings) == 1

        zt_seg_findings = Finding.objects(test=zero_trust_consts.TEST_SEGMENTATION)
        assert len(zt_seg_findings) == 2
